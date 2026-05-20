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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/self_serving_bias_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    outcome_valence = factor(outcome_valence),
    actor_target = factor(actor_target),
    self_other = factor(self_other),
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, outcome_valence, self_other) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_internal = mean(internal_attribution, na.rm = TRUE),
    mean_external = mean(external_attribution, na.rm = TRUE),
    mean_responsibility = mean(responsibility_rating, na.rm = TRUE),
    mean_blame = mean(blame_rating, na.rm = TRUE),
    mean_credit = mean(credit_claiming, na.rm = TRUE),
    mean_excuse = mean(excuse_making, na.rm = TRUE),
    mean_ego_threat = mean(ego_threat, na.rm = TRUE),
    mean_learning = mean(learning_intention, na.rm = TRUE),
    mean_accountability = mean(accountability_pressure, na.rm = TRUE),
    mean_evidence = mean(evidence_strength, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_valence_self_other.csv"))

internal_model <- lmer(
  internal_attribution ~
    outcome_valence * self_other +
    ego_threat +
    self_esteem +
    task_importance +
    evidence_strength +
    accountability_pressure +
    condition +
    actor_target +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

external_model <- lmer(
  external_attribution ~
    outcome_valence * self_other +
    ego_threat +
    self_esteem +
    task_importance +
    evidence_strength +
    accountability_pressure +
    condition +
    actor_target +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

responsibility_model <- lmer(
  responsibility_rating ~
    internal_attribution +
    external_attribution +
    controllable_attribution +
    outcome_valence * self_other +
    evidence_strength +
    accountability_pressure +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

blame_model <- lmer(
  blame_rating ~
    outcome_valence * self_other +
    internal_attribution +
    external_attribution +
    responsibility_rating +
    ego_threat +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

credit_model <- lmer(
  credit_claiming ~
    outcome_valence * self_other +
    internal_attribution +
    self_esteem +
    ego_threat +
    accountability_pressure +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

excuse_model <- lmer(
  excuse_making ~
    outcome_valence * self_other +
    external_attribution +
    ego_threat +
    evidence_strength +
    accountability_pressure +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

learning_model <- lmer(
  learning_intention ~
    responsibility_rating +
    excuse_making +
    evidence_strength +
    accountability_pressure +
    outcome_valence +
    self_other +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    outcome_valence * self_other +
    ego_threat +
    task_importance +
    evidence_strength +
    accountability_pressure +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

bias_scores <- dat %>%
  filter(outcome_valence %in% c("positive", "negative")) %>%
  group_by(participant, self_other, outcome_valence) %>%
  summarise(
    mean_internal = mean(internal_attribution, na.rm = TRUE),
    mean_external = mean(external_attribution, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  pivot_wider(
    names_from = outcome_valence,
    values_from = c(mean_internal, mean_external)
  ) %>%
  mutate(
    ssb_internal = mean_internal_positive - mean_internal_negative,
    ssb_external = mean_external_negative - mean_external_positive,
    ssb_full = ssb_internal + ssb_external
  )

write_csv(bias_scores, file.path(output_dir, "r_self_serving_bias_scores.csv"))

capture.output(
  list(
    internal_attribution_model = summary(internal_model),
    external_attribution_model = summary(external_model),
    responsibility_model = summary(responsibility_model),
    blame_model = summary(blame_model),
    credit_model = summary(credit_model),
    excuse_model = summary(excuse_model),
    learning_model = summary(learning_model),
    response_time_model = summary(rt_model),
    internal_emmeans = emmeans(internal_model, ~ outcome_valence * self_other),
    external_emmeans = emmeans(external_model, ~ outcome_valence * self_other),
    diagnostics = check_model(internal_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(internal_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_internal_attribution_coefficients.csv"))
write_csv(tidy(external_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_external_attribution_coefficients.csv"))
write_csv(tidy(responsibility_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_responsibility_coefficients.csv"))
write_csv(tidy(excuse_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_excuse_coefficients.csv"))
write_csv(tidy(learning_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_learning_coefficients.csv"))

p <- ggplot(dat, aes(x = internal_attribution, y = responsibility_rating, color = outcome_valence)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Internal attribution and responsibility judgment",
    x = "Internal attribution",
    y = "Responsibility rating"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_internal_attribution_responsibility_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
