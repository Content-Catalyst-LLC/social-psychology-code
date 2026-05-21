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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/altruism_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    recipient_id = factor(recipient_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    condition = factor(condition),
    context_type = factor(context_type),
    altruistic_decision = as.integer(altruistic_decision),
    altruistic_punishment = as.integer(altruistic_punishment),
    other_regarding_weight = (
      empathy_score +
      recipient_need +
      identity_overlap +
      moral_identity +
      perceived_efficacy -
      helping_cost -
      intervention_risk
    ) / 5,
    egoistic_reward_index = (
      reciprocity_expectation +
      reputation_visibility +
      warm_glow_expectation
    ) / 3,
    cost_pressure_index = (
      helping_cost +
      intervention_risk +
      personal_distress
    ) / 3,
    inclusive_fitness_score = kinship_coefficient * recipient_need - helping_cost / 10,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, context_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    altruism_rate = mean(altruistic_decision, na.rm = TRUE),
    punishment_rate = mean(altruistic_punishment, na.rm = TRUE),
    mean_donation = mean(donation_amount, na.rm = TRUE),
    mean_volunteer_minutes = mean(time_volunteered_minutes, na.rm = TRUE),
    mean_public_goods = mean(public_goods_contribution, na.rm = TRUE),
    mean_empathy = mean(empathy_score, na.rm = TRUE),
    mean_cost = mean(helping_cost, na.rm = TRUE),
    mean_recipient_need = mean(recipient_need, na.rm = TRUE),
    mean_identity_overlap = mean(identity_overlap, na.rm = TRUE),
    mean_moral_identity = mean(moral_identity, na.rm = TRUE),
    mean_efficacy = mean(perceived_efficacy, na.rm = TRUE),
    mean_other_regarding_weight = mean(other_regarding_weight, na.rm = TRUE),
    mean_egoistic_reward = mean(egoistic_reward_index, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

altruistic_decision_model <- glmer(
  altruistic_decision ~
    empathy_score +
    personal_distress +
    helping_cost +
    recipient_need +
    recipient_closeness +
    identity_overlap +
    kinship_coefficient +
    reciprocity_expectation +
    reputation_visibility +
    moral_identity +
    social_norm_salience +
    warm_glow_expectation +
    perceived_efficacy +
    intervention_risk +
    condition +
    context_type +
    (1 | participant) +
    (1 | recipient_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

donation_model <- lmer(
  donation_amount ~
    empathy_score +
    helping_cost +
    recipient_need +
    recipient_closeness +
    identity_overlap +
    reciprocity_expectation +
    reputation_visibility +
    moral_identity +
    social_norm_salience +
    warm_glow_expectation +
    perceived_efficacy +
    intervention_risk +
    altruistic_decision +
    condition +
    context_type +
    (1 | participant) +
    (1 | recipient_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

public_goods_model <- lmer(
  public_goods_contribution ~
    social_norm_salience +
    perceived_efficacy +
    moral_identity +
    reciprocity_expectation +
    reputation_visibility +
    warm_glow_expectation +
    helping_cost +
    altruistic_decision +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

punishment_model <- glmer(
  altruistic_punishment ~
    social_norm_salience +
    moral_identity +
    identity_overlap +
    personal_distress +
    perceived_efficacy +
    punishment_cost +
    helping_cost +
    intervention_risk +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

response_time_model <- lmer(
  log_response_time ~
    empathy_score +
    helping_cost +
    personal_distress +
    recipient_need +
    perceived_efficacy +
    intervention_risk +
    altruistic_decision +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    altruistic_decision_model = summary(altruistic_decision_model),
    donation_model = summary(donation_model),
    public_goods_model = summary(public_goods_model),
    punishment_model = summary(punishment_model),
    response_time_model = summary(response_time_model),
    condition_decision_rates = emmeans(altruistic_decision_model, ~ condition, type = "response"),
    diagnostics = check_model(donation_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(altruistic_decision_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_altruistic_decision_coefficients.csv"))
write_csv(tidy(donation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_donation_coefficients.csv"))
write_csv(tidy(public_goods_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_public_goods_coefficients.csv"))
write_csv(tidy(punishment_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_punishment_coefficients.csv"))

cost_summary <- dat %>%
  mutate(
    cost_band = cut(
      helping_cost,
      breaks = c(-0.1, 2.5, 5, 7.5, 10.1),
      labels = c("low_cost", "moderate_cost", "high_cost", "very_high_cost")
    )
  ) %>%
  group_by(condition, cost_band) %>%
  summarise(
    n = n(),
    altruism_rate = mean(altruistic_decision, na.rm = TRUE),
    mean_donation = mean(donation_amount, na.rm = TRUE),
    mean_public_goods = mean(public_goods_contribution, na.rm = TRUE),
    mean_empathy = mean(empathy_score, na.rm = TRUE),
    mean_efficacy = mean(perceived_efficacy, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(cost_summary, file.path(output_dir, "r_summary_by_condition_cost_band.csv"))

p <- ggplot(cost_summary, aes(x = cost_band, y = altruism_rate, color = condition, group = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Altruistic decisions by helping cost and condition",
    x = "Helping-cost band",
    y = "Altruistic decision rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_altruism_by_cost_band_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
