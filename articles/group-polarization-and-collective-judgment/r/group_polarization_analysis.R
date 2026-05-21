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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/group_polarization_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    group_id = factor(group_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    platform_context = factor(platform_context),
    condition = factor(condition),
    attitude_shift = post_attitude - pre_attitude,
    extremity_shift = abs(post_attitude) - abs(pre_attitude),
    confidence_shift = post_confidence - pre_confidence,
    directional_polarization = as.integer(
      abs(post_attitude) > abs(pre_attitude) &
      sign(post_attitude) == sign(pre_attitude)
    ),
    polarization_risk_index = (
      argument_exposure +
      informational_homogeneity +
      social_comparison_pressure +
      identity_salience +
      group_identification +
      norm_enforcement +
      algorithmic_reinforcement -
      argument_diversity -
      dissent_quality -
      minority_view_protection -
      deliberation_structure -
      cross_cutting_exposure
    ) / 6,
    deliberative_safeguard_index = (
      argument_diversity +
      dissent_quality +
      minority_view_protection +
      deliberation_structure +
      moderation_quality +
      cross_cutting_exposure +
      perceived_legitimacy
    ) / 7,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, platform_context) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    groups = n_distinct(group_id),
    mean_pre_attitude = mean(pre_attitude, na.rm = TRUE),
    mean_post_attitude = mean(post_attitude, na.rm = TRUE),
    mean_shift = mean(attitude_shift, na.rm = TRUE),
    mean_extremity_shift = mean(extremity_shift, na.rm = TRUE),
    directional_polarization_rate = mean(directional_polarization, na.rm = TRUE),
    mean_confidence_shift = mean(confidence_shift, na.rm = TRUE),
    mean_argument_exposure = mean(argument_exposure, na.rm = TRUE),
    mean_argument_diversity = mean(argument_diversity, na.rm = TRUE),
    mean_homogeneity = mean(informational_homogeneity, na.rm = TRUE),
    mean_identity_salience = mean(identity_salience, na.rm = TRUE),
    mean_dissent_quality = mean(dissent_quality, na.rm = TRUE),
    mean_safeguards = mean(deliberative_safeguard_index, na.rm = TRUE),
    mean_decision_quality = mean(decision_quality, na.rm = TRUE),
    mean_accuracy = mean(collective_judgment_accuracy, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

extremity_model <- lmer(
  extremity_shift ~
    argument_exposure +
    argument_diversity +
    informational_homogeneity +
    social_comparison_pressure +
    identity_salience +
    group_identification +
    norm_enforcement +
    dissent_presence +
    dissent_quality +
    minority_view_protection +
    deliberation_structure +
    moderation_quality +
    algorithmic_reinforcement +
    cross_cutting_exposure +
    perceived_legitimacy +
    condition +
    platform_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

confidence_model <- lmer(
  confidence_shift ~
    argument_exposure +
    informational_homogeneity +
    social_comparison_pressure +
    identity_salience +
    group_identification +
    norm_enforcement +
    argument_diversity +
    dissent_quality +
    deliberation_structure +
    cross_cutting_exposure +
    condition +
    platform_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

decision_quality_model <- lmer(
  decision_quality ~
    polarization_risk_index +
    deliberative_safeguard_index +
    argument_diversity +
    dissent_quality +
    minority_view_protection +
    deliberation_structure +
    algorithmic_reinforcement +
    cross_cutting_exposure +
    perceived_legitimacy +
    abs(post_attitude) +
    condition +
    platform_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

accuracy_model <- lmer(
  collective_judgment_accuracy ~
    polarization_risk_index +
    deliberative_safeguard_index +
    informational_homogeneity +
    norm_enforcement +
    algorithmic_reinforcement +
    cross_cutting_exposure +
    perceived_legitimacy +
    abs(post_attitude) +
    condition +
    platform_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    abs(post_attitude) +
    identity_salience +
    social_comparison_pressure +
    informational_homogeneity +
    deliberation_structure +
    argument_diversity +
    dissent_quality +
    condition +
    platform_context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    extremity_model = summary(extremity_model),
    confidence_model = summary(confidence_model),
    decision_quality_model = summary(decision_quality_model),
    accuracy_model = summary(accuracy_model),
    response_time_model = summary(response_time_model),
    condition_extremity = emmeans(extremity_model, ~ condition),
    diagnostics = check_model(extremity_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(extremity_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_extremity_shift_coefficients.csv"))
write_csv(tidy(confidence_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_confidence_shift_coefficients.csv"))
write_csv(tidy(decision_quality_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_decision_quality_coefficients.csv"))
write_csv(tidy(accuracy_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_accuracy_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_extremity_shift = mean(extremity_shift, na.rm = TRUE),
    directional_polarization_rate = mean(directional_polarization, na.rm = TRUE),
    mean_confidence_shift = mean(confidence_shift, na.rm = TRUE),
    mean_decision_quality = mean(decision_quality, na.rm = TRUE),
    mean_accuracy = mean(collective_judgment_accuracy, na.rm = TRUE),
    mean_risk = mean(polarization_risk_index, na.rm = TRUE),
    mean_safeguards = mean(deliberative_safeguard_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_summary_by_condition.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_extremity_shift), y = mean_extremity_shift, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean extremity shift by discussion condition",
    x = "Condition",
    y = "Mean extremity shift"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_extremity_shift_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
