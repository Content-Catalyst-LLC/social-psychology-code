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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/heuristics_biases_trials.csv")
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
    judgment_domain = factor(judgment_domain),
    heuristic_type = factor(heuristic_type),
    condition = factor(condition),
    frame_type = factor(frame_type),
    anchoring_error = estimate - true_value,
    absolute_error = abs(anchoring_error),
    calibration_error = abs(confidence_rating - actual_accuracy),
    log_response_time = log(response_time_ms),
    bias_pressure_index = (
      availability_salience +
      representativeness_rating +
      confirmation_tendency +
      abs(affect_valence) -
      debiasing_intervention_strength -
      institutional_accountability -
      feedback_quality
    ) / 4,
    evidence_discipline_index = (
      debiasing_intervention_strength +
      institutional_accountability +
      feedback_quality +
      disconfirming_evidence_exposure
    ) / 4
  )

summary_table <- dat %>%
  group_by(heuristic_type, condition) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_estimate = mean(estimate, na.rm = TRUE),
    mean_true_value = mean(true_value, na.rm = TRUE),
    mean_anchoring_error = mean(anchoring_error, na.rm = TRUE),
    mean_absolute_error = mean(absolute_error, na.rm = TRUE),
    mean_calibration_error = mean(calibration_error, na.rm = TRUE),
    mean_overconfidence = mean(overconfidence_score, na.rm = TRUE),
    mean_decision_quality = mean(decision_quality, na.rm = TRUE),
    mean_bias_pressure = mean(bias_pressure_index, na.rm = TRUE),
    mean_evidence_discipline = mean(evidence_discipline_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_heuristic_condition.csv"))

anchor_model <- lmer(
  anchoring_error ~
    anchor_value +
    true_value +
    heuristic_type +
    condition +
    debiasing_intervention_strength +
    institutional_accountability +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

calibration_model <- lmer(
  calibration_error ~
    confidence_rating +
    actual_accuracy +
    heuristic_type +
    condition +
    feedback_quality +
    debiasing_intervention_strength +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

risk_model <- lmer(
  perceived_risk ~
    availability_salience +
    affect_valence +
    representativeness_rating +
    confirmation_tendency +
    debiasing_intervention_strength +
    condition +
    judgment_domain +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

decision_quality_model <- lmer(
  decision_quality ~
    absolute_error +
    calibration_error +
    debiasing_intervention_strength +
    institutional_accountability +
    feedback_quality +
    disconfirming_evidence_exposure +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    availability_salience +
    absolute_error +
    debiasing_intervention_strength +
    institutional_accountability +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    anchor_model = summary(anchor_model),
    calibration_model = summary(calibration_model),
    risk_model = summary(risk_model),
    decision_quality_model = summary(decision_quality_model),
    response_time_model = summary(response_time_model),
    anchor_emmeans = emmeans(anchor_model, ~ condition),
    diagnostics = check_model(anchor_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(anchor_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_anchor_coefficients.csv"))
write_csv(tidy(calibration_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_calibration_coefficients.csv"))
write_csv(tidy(decision_quality_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_decision_quality_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_absolute_error = mean(absolute_error, na.rm = TRUE),
    mean_calibration_error = mean(calibration_error, na.rm = TRUE),
    mean_overconfidence = mean(overconfidence_score, na.rm = TRUE),
    mean_decision_quality = mean(decision_quality, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_condition_summary.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_decision_quality), y = mean_decision_quality, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean decision quality by condition",
    x = "Condition",
    y = "Mean decision quality"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_decision_quality_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
