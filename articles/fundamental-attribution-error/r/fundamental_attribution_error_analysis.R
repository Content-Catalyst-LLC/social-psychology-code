#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(tidyverse)
  library(lme4)
  library(lmerTest)
  library(emmeans)
  library(broom.mixed)
  library(performance)
})

args <- commandArgs(trailingOnly = TRUE)
input_path <- ifelse(length(args) >= 1, args[[1]], "data/fundamental_attribution_error_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    actor_role = factor(actor_role),
    observer_role = factor(observer_role),
    behavior_valence = factor(behavior_valence),
    fae_score = dispositional_attribution - situational_attribution,
    constraint_neglect = actual_constraint - perceived_constraint,
    correspondence_bias_score = correspondence_inference - choice_freedom,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, behavior_valence) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_dispositional = mean(dispositional_attribution, na.rm = TRUE),
    mean_situational = mean(situational_attribution, na.rm = TRUE),
    mean_fae_score = mean(fae_score, na.rm = TRUE),
    mean_constraint_neglect = mean(constraint_neglect, na.rm = TRUE),
    mean_correspondence_bias = mean(correspondence_bias_score, na.rm = TRUE),
    mean_blame = mean(moral_blame, na.rm = TRUE),
    mean_punishment = mean(punishment_recommendation, na.rm = TRUE),
    mean_empathy = mean(empathy, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_valence.csv"))

disposition_model <- lmer(
  dispositional_attribution ~
    perceived_constraint +
    choice_freedom +
    cognitive_load +
    perspective_taking +
    accountability_pressure +
    evidence_strength +
    cultural_individualism +
    structural_awareness +
    condition +
    behavior_valence +
    actor_role +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

situation_model <- lmer(
  situational_attribution ~
    perceived_constraint +
    actual_constraint +
    choice_freedom +
    cognitive_load +
    perspective_taking +
    accountability_pressure +
    evidence_strength +
    cultural_individualism +
    structural_awareness +
    condition +
    behavior_valence +
    actor_role +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

correspondence_model <- lmer(
  correspondence_inference ~
    dispositional_attribution +
    situational_attribution +
    perceived_constraint +
    choice_freedom +
    condition +
    behavior_valence +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

fae_model <- lmer(
  fae_score ~
    cognitive_load +
    perspective_taking +
    accountability_pressure +
    perceived_constraint +
    choice_freedom +
    cultural_individualism +
    structural_awareness +
    condition +
    behavior_valence +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

blame_model <- lmer(
  moral_blame ~
    dispositional_attribution +
    situational_attribution +
    empathy +
    behavior_valence +
    actor_role +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

punishment_model <- lmer(
  punishment_recommendation ~
    moral_blame +
    dispositional_attribution +
    situational_attribution +
    empathy +
    accountability_pressure +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    cognitive_load +
    evidence_strength +
    perceived_constraint +
    choice_freedom +
    fae_score +
    condition +
    behavior_valence +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    disposition_model = summary(disposition_model),
    situation_model = summary(situation_model),
    correspondence_model = summary(correspondence_model),
    fae_model = summary(fae_model),
    blame_model = summary(blame_model),
    punishment_model = summary(punishment_model),
    response_time_model = summary(rt_model),
    dispositional_by_condition = emmeans(disposition_model, ~ condition),
    fae_by_condition = emmeans(fae_model, ~ condition),
    diagnostics = check_model(fae_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(disposition_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_dispositional_coefficients.csv"))
write_csv(tidy(situation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_situational_coefficients.csv"))
write_csv(tidy(fae_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_fae_score_coefficients.csv"))
write_csv(tidy(blame_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_blame_coefficients.csv"))
write_csv(tidy(punishment_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_punishment_coefficients.csv"))

p <- ggplot(dat, aes(x = perceived_constraint, y = dispositional_attribution, color = condition)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Perceived constraint and dispositional attribution",
    x = "Perceived constraint",
    y = "Dispositional attribution"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_constraint_disposition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
