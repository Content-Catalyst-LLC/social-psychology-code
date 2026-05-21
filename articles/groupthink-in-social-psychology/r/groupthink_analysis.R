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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/groupthink_trials.csv")
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
    condition = factor(condition),
    symptom_index = (
      illusion_invulnerability +
      collective_rationalization +
      inherent_morality +
      outgroup_stereotyping +
      self_censorship +
      direct_pressure_dissenters +
      mindguarding
    ) / 7,
    antecedent_risk_index = (
      cohesion +
      leadership_directive +
      group_insulation +
      stress_level +
      consensus_pressure
    ) / 5,
    process_quality_index = (
      dissent_visibility +
      outside_information +
      alternative_search +
      risk_analysis +
      contingency_planning +
      leader_impartiality +
      psychological_safety
    ) / 7,
    safeguard_index = (
      dissent_visibility +
      outside_information +
      alternative_search +
      risk_analysis +
      contingency_planning +
      leader_impartiality +
      psychological_safety +
      2 * devils_advocate +
      2 * independent_expert_consulted +
      2 * subgroup_review
    ) / 9,
    unanimity_gap = perceived_unanimity - (100 - private_disagreement),
    groupthink_risk_index = antecedent_risk_index + symptom_index - process_quality_index,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, institution_context) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    groups = n_distinct(group_id),
    mean_groupthink_risk = mean(groupthink_risk_index, na.rm = TRUE),
    mean_antecedent_risk = mean(antecedent_risk_index, na.rm = TRUE),
    mean_symptoms = mean(symptom_index, na.rm = TRUE),
    mean_process_quality = mean(process_quality_index, na.rm = TRUE),
    mean_safeguards = mean(safeguard_index, na.rm = TRUE),
    mean_unanimity_gap = mean(unanimity_gap, na.rm = TRUE),
    mean_self_censorship = mean(self_censorship, na.rm = TRUE),
    mean_dissent_visibility = mean(dissent_visibility, na.rm = TRUE),
    mean_outside_information = mean(outside_information, na.rm = TRUE),
    mean_decision_quality = mean(decision_quality, na.rm = TRUE),
    mean_forecast_calibration = mean(forecast_calibration, na.rm = TRUE),
    mean_implementation_risk = mean(implementation_risk, na.rm = TRUE),
    mean_review_quality = mean(post_decision_review_quality, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

decision_quality_model <- lmer(
  decision_quality ~
    groupthink_risk_index +
    safeguard_index +
    cohesion +
    leadership_directive +
    group_insulation +
    stress_level +
    consensus_pressure +
    dissent_visibility +
    outside_information +
    alternative_search +
    risk_analysis +
    contingency_planning +
    leader_impartiality +
    psychological_safety +
    condition +
    institution_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

self_censorship_model <- lmer(
  self_censorship ~
    cohesion +
    leadership_directive +
    group_insulation +
    stress_level +
    consensus_pressure +
    dissent_visibility +
    leader_impartiality +
    psychological_safety +
    condition +
    institution_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

forecast_model <- lmer(
  forecast_calibration ~
    groupthink_risk_index +
    safeguard_index +
    outside_information +
    risk_analysis +
    illusion_invulnerability +
    collective_rationalization +
    condition +
    institution_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

implementation_risk_model <- lmer(
  implementation_risk ~
    groupthink_risk_index +
    symptom_index +
    risk_analysis +
    contingency_planning +
    outside_information +
    safeguard_index +
    condition +
    institution_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    stress_level +
    consensus_pressure +
    self_censorship +
    alternative_search +
    risk_analysis +
    condition +
    institution_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    decision_quality_model = summary(decision_quality_model),
    self_censorship_model = summary(self_censorship_model),
    forecast_model = summary(forecast_model),
    implementation_risk_model = summary(implementation_risk_model),
    response_time_model = summary(response_time_model),
    condition_quality = emmeans(decision_quality_model, ~ condition),
    diagnostics = check_model(decision_quality_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(decision_quality_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_decision_quality_coefficients.csv"))
write_csv(tidy(self_censorship_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_self_censorship_coefficients.csv"))
write_csv(tidy(forecast_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_forecast_coefficients.csv"))
write_csv(tidy(implementation_risk_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_implementation_risk_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_groupthink_risk = mean(groupthink_risk_index, na.rm = TRUE),
    mean_self_censorship = mean(self_censorship, na.rm = TRUE),
    mean_unanimity_gap = mean(unanimity_gap, na.rm = TRUE),
    mean_decision_quality = mean(decision_quality, na.rm = TRUE),
    mean_forecast_calibration = mean(forecast_calibration, na.rm = TRUE),
    mean_implementation_risk = mean(implementation_risk, na.rm = TRUE),
    mean_safeguards = mean(safeguard_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_summary_by_condition.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_groupthink_risk), y = mean_groupthink_risk, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean groupthink-risk index by condition",
    x = "Condition",
    y = "Mean groupthink-risk index"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_groupthink_risk_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
