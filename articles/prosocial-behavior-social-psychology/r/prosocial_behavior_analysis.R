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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/prosocial_behavior_trials.csv")
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
    helping_decision = as.integer(helping_decision),
    emotional_support = as.integer(emotional_support),
    log_bystanders = log1p(bystander_count),
    prosocial_motivation_index = (
      empathy_score +
      perspective_taking +
      norm_salience +
      efficacy_belief +
      felt_responsibility +
      moral_identity -
      helping_cost -
      intervention_risk
    ) / 6,
    social_embeddedness_index = (
      identity_overlap +
      group_identification +
      trust_level +
      institutional_legitimacy +
      reciprocity_expectation
    ) / 5,
    cost_pressure_index = (
      helping_cost +
      intervention_risk +
      log_bystanders
    ) / 3,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, context_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    helping_rate = mean(helping_decision, na.rm = TRUE),
    emotional_support_rate = mean(emotional_support, na.rm = TRUE),
    mean_donation = mean(donation_amount, na.rm = TRUE),
    mean_volunteer_minutes = mean(volunteer_minutes, na.rm = TRUE),
    mean_cooperation = mean(cooperation_contribution, na.rm = TRUE),
    mean_empathy = mean(empathy_score, na.rm = TRUE),
    mean_norms = mean(norm_salience, na.rm = TRUE),
    mean_efficacy = mean(efficacy_belief, na.rm = TRUE),
    mean_cost = mean(helping_cost, na.rm = TRUE),
    mean_bystanders = mean(bystander_count, na.rm = TRUE),
    mean_responsibility = mean(felt_responsibility, na.rm = TRUE),
    mean_identity = mean(identity_overlap, na.rm = TRUE),
    mean_legitimacy = mean(institutional_legitimacy, na.rm = TRUE),
    mean_prosocial_motivation = mean(prosocial_motivation_index, na.rm = TRUE),
    mean_social_embeddedness = mean(social_embeddedness_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

helping_model <- glmer(
  helping_decision ~
    empathy_score +
    perspective_taking +
    norm_salience +
    reciprocity_expectation +
    efficacy_belief +
    helping_cost +
    intervention_risk +
    log_bystanders +
    felt_responsibility +
    identity_overlap +
    group_identification +
    trust_level +
    moral_identity +
    reputation_visibility +
    institutional_legitimacy +
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
    norm_salience +
    efficacy_belief +
    helping_cost +
    intervention_risk +
    felt_responsibility +
    identity_overlap +
    moral_identity +
    reputation_visibility +
    institutional_legitimacy +
    helping_decision +
    condition +
    context_type +
    (1 | participant) +
    (1 | recipient_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

cooperation_model <- lmer(
  cooperation_contribution ~
    norm_salience +
    efficacy_belief +
    reciprocity_expectation +
    group_identification +
    trust_level +
    institutional_legitimacy +
    helping_cost +
    helping_decision +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

emotional_support_model <- glmer(
  emotional_support ~
    empathy_score +
    perspective_taking +
    norm_salience +
    identity_overlap +
    intervention_risk +
    condition +
    context_type +
    (1 | participant) +
    (1 | recipient_id) +
    (1 | scenario_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

response_time_model <- lmer(
  log_response_time ~
    empathy_score +
    norm_salience +
    efficacy_belief +
    helping_cost +
    intervention_risk +
    log_bystanders +
    felt_responsibility +
    helping_decision +
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
    helping_model = summary(helping_model),
    donation_model = summary(donation_model),
    cooperation_model = summary(cooperation_model),
    emotional_support_model = summary(emotional_support_model),
    response_time_model = summary(response_time_model),
    condition_helping_rates = emmeans(helping_model, ~ condition, type = "response"),
    diagnostics = check_model(donation_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(helping_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_helping_coefficients.csv"))
write_csv(tidy(donation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_donation_coefficients.csv"))
write_csv(tidy(cooperation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_cooperation_coefficients.csv"))
write_csv(tidy(emotional_support_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_emotional_support_coefficients.csv"))

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
    helping_rate = mean(helping_decision, na.rm = TRUE),
    mean_donation = mean(donation_amount, na.rm = TRUE),
    mean_cooperation = mean(cooperation_contribution, na.rm = TRUE),
    mean_efficacy = mean(efficacy_belief, na.rm = TRUE),
    mean_responsibility = mean(felt_responsibility, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(cost_summary, file.path(output_dir, "r_summary_by_condition_cost_band.csv"))

p <- ggplot(cost_summary, aes(x = cost_band, y = helping_rate, color = condition, group = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Prosocial helping by cost band and condition",
    x = "Helping-cost band",
    y = "Helping rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_helping_by_cost_band_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
