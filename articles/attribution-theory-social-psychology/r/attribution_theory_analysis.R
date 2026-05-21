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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/attribution_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    group_id = factor(group_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    institution_context = factor(institution_context),
    behavior_domain = factor(behavior_domain),
    target_type = factor(target_type),
    self_other = factor(self_other),
    outcome_valence = factor(outcome_valence),
    condition = factor(condition),
    log_response_time = log(response_time_ms),
    disposition_bias_index = attribution_internal - attribution_external,
    covariation_situation_index = (consensus + distinctiveness + consistency) / 3,
    responsibility_inference_index = (
      intentionality + perceived_choice + controllability_rating - situational_constraint
    ) / 3,
    system_visible_attribution_index = attribution_external + 2 * attributional_complexity
  )

summary_table <- dat %>%
  group_by(condition, target_type, outcome_valence) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_internal = mean(attribution_internal, na.rm = TRUE),
    mean_external = mean(attribution_external, na.rm = TRUE),
    mean_responsibility = mean(responsibility_rating, na.rm = TRUE),
    mean_blame = mean(blame_rating, na.rm = TRUE),
    mean_sympathy = mean(sympathy_rating, na.rm = TRUE),
    mean_punishment = mean(punishment_support, na.rm = TRUE),
    mean_help = mean(help_support, na.rm = TRUE),
    mean_hostile = mean(hostile_attribution_score, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_target_valence.csv"))

internal_model <- lmer(
  attribution_internal ~
    ambiguity_level +
    intentionality +
    perceived_choice +
    perceived_effort +
    perceived_ability +
    situational_constraint +
    consensus +
    distinctiveness +
    consistency +
    target_type +
    outcome_valence +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

external_model <- lmer(
  attribution_external ~
    ambiguity_level +
    situational_constraint +
    consensus +
    distinctiveness +
    consistency +
    intentionality +
    perceived_choice +
    attributional_complexity +
    target_type +
    outcome_valence +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

responsibility_model <- lmer(
  responsibility_rating ~
    attribution_internal +
    attribution_external +
    intentionality +
    perceived_choice +
    controllability_rating +
    situational_constraint +
    outcome_valence +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

hostile_model <- lmer(
  hostile_attribution_score ~
    ambiguity_level +
    target_type +
    outcome_valence +
    situational_constraint +
    attributional_complexity +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

achievement_model <- lmer(
  achievement_expectation ~
    perceived_effort +
    perceived_ability +
    stability_rating +
    controllability_rating +
    situational_constraint +
    outcome_valence +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    ambiguity_level +
    attribution_internal +
    attribution_external +
    attributional_complexity +
    target_type +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    internal_model = summary(internal_model),
    external_model = summary(external_model),
    responsibility_model = summary(responsibility_model),
    hostile_model = summary(hostile_model),
    achievement_model = summary(achievement_model),
    response_time_model = summary(response_time_model),
    target_responsibility = emmeans(responsibility_model, ~ target_type + outcome_valence),
    diagnostics = check_model(responsibility_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(internal_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_internal_attribution_coefficients.csv"))
write_csv(tidy(external_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_external_attribution_coefficients.csv"))
write_csv(tidy(responsibility_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_responsibility_coefficients.csv"))
write_csv(tidy(hostile_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_hostile_attribution_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_internal = mean(attribution_internal, na.rm = TRUE),
    mean_external = mean(attribution_external, na.rm = TRUE),
    mean_responsibility = mean(responsibility_rating, na.rm = TRUE),
    mean_blame = mean(blame_rating, na.rm = TRUE),
    mean_help = mean(help_support, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_condition_summary.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_responsibility), y = mean_responsibility, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean responsibility judgment by attribution condition",
    x = "Condition",
    y = "Mean responsibility judgment"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_responsibility_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
