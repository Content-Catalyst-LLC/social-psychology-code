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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/dissonance_trials.csv")
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
    paradigm = factor(paradigm),
    condition = factor(condition),
    attitude_change = post_attitude - pre_attitude,
    spreading_of_alternatives = (chosen_post_value - chosen_pre_value) -
      (rejected_post_value - rejected_pre_value),
    log_response_time = log(response_time_ms),
    dissonance_magnitude_index = (
      counter_attitudinal_behavior +
      perceived_choice +
      perceived_responsibility +
      identity_threat +
      public_commitment -
      external_justification -
      self_affirmation
    ) / 5,
    institutional_escalation_index = (
      sunk_cost +
      public_commitment +
      institutional_identity_threat -
      evidence_strength -
      accountability
    ) / 3
  )

summary_table <- dat %>%
  group_by(paradigm, condition) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_attitude_change = mean(attitude_change, na.rm = TRUE),
    mean_spreading = mean(spreading_of_alternatives, na.rm = TRUE),
    mean_outcome_value = mean(outcome_value, na.rm = TRUE),
    mean_proselytizing = mean(proselytizing_intensity, na.rm = TRUE),
    mean_coherence_pressure = mean(coherence_pressure, na.rm = TRUE),
    mean_discomfort = mean(dissonance_discomfort, na.rm = TRUE),
    mean_policy_reversal = mean(policy_reversal_willingness, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_paradigm_condition.csv"))

attitude_model <- lmer(
  attitude_change ~
    paradigm +
    condition +
    counter_attitudinal_behavior +
    perceived_choice +
    perceived_responsibility +
    identity_threat +
    self_affirmation +
    external_justification +
    public_commitment +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

spread_model <- lmer(
  spreading_of_alternatives ~
    perceived_choice +
    public_commitment +
    identity_threat +
    self_affirmation +
    external_justification +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

effort_model <- lmer(
  outcome_value ~
    effort_cost +
    commitment_strength +
    public_commitment +
    identity_threat +
    self_affirmation +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

belief_model <- lmer(
  proselytizing_intensity ~
    belief_disconfirmation_strength +
    commitment_strength +
    public_commitment +
    identity_threat +
    self_affirmation +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    coherence_pressure +
    identity_threat +
    belief_disconfirmation_strength +
    self_affirmation +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

institutional_model <- lmer(
  policy_reversal_willingness ~
    evidence_strength +
    accountability +
    sunk_cost +
    public_commitment +
    institutional_identity_threat +
    condition +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

capture.output(
  list(
    attitude_model = summary(attitude_model),
    spread_model = summary(spread_model),
    effort_model = summary(effort_model),
    belief_model = summary(belief_model),
    rt_model = summary(rt_model),
    institutional_model = summary(institutional_model),
    paradigm_condition = emmeans(attitude_model, ~ paradigm + condition),
    diagnostics = check_model(attitude_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(attitude_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_attitude_change_coefficients.csv"))
write_csv(tidy(spread_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_spreading_coefficients.csv"))
write_csv(tidy(institutional_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_institutional_reversal_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_attitude_change = mean(attitude_change, na.rm = TRUE),
    mean_spreading = mean(spreading_of_alternatives, na.rm = TRUE),
    mean_dissonance_discomfort = mean(dissonance_discomfort, na.rm = TRUE),
    mean_policy_reversal = mean(policy_reversal_willingness, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_condition_summary.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_attitude_change), y = mean_attitude_change, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean attitude change by dissonance condition",
    x = "Condition",
    y = "Mean attitude change"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_attitude_change_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
