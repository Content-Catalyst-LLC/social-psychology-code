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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/social_norms_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    reference_group = factor(reference_group),
    policy_domain = factor(policy_domain),
    condition = factor(condition),
    message_type = factor(message_type),
    complied = as.integer(complied),
    reported_violation = as.integer(reported_violation),
    norm_strength_index = (
      descriptive_norm +
      injunctive_norm +
      empirical_expectation +
      normative_expectation
    ) / 4,
    enforcement_index = (
      sanction_salience +
      sanction_severity +
      reward_salience
    ) / 3,
    legitimacy_trust_index = (
      institutional_legitimacy +
      trust_in_institution
    ) / 2,
    tipping_margin = tipping_exposure - norm_threshold,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, policy_domain, message_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    compliance_rate = mean(complied, na.rm = TRUE),
    reporting_rate = mean(reported_violation, na.rm = TRUE),
    mean_intention = mean(compliance_intention, na.rm = TRUE),
    mean_contribution = mean(contribution_amount, na.rm = TRUE),
    mean_descriptive = mean(descriptive_norm, na.rm = TRUE),
    mean_injunctive = mean(injunctive_norm, na.rm = TRUE),
    mean_empirical = mean(empirical_expectation, na.rm = TRUE),
    mean_normative = mean(normative_expectation, na.rm = TRUE),
    mean_personal_attitude = mean(personal_attitude, na.rm = TRUE),
    mean_pluralistic_ignorance = mean(pluralistic_ignorance, na.rm = TRUE),
    mean_norm_strength = mean(norm_strength_index, na.rm = TRUE),
    mean_enforcement = mean(enforcement_index, na.rm = TRUE),
    mean_legitimacy_trust = mean(legitimacy_trust_index, na.rm = TRUE),
    mean_tipping_margin = mean(tipping_margin, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_domain_message.csv"))

compliance_model <- glmer(
  complied ~
    descriptive_norm +
    injunctive_norm +
    empirical_expectation +
    normative_expectation +
    personal_attitude +
    norm_salience +
    sanction_salience +
    sanction_severity +
    reward_salience +
    reference_group_identification +
    institutional_legitimacy +
    trust_in_institution +
    pluralistic_ignorance +
    dynamic_norm_trend +
    tipping_margin +
    condition +
    policy_domain +
    message_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

intention_model <- lmer(
  compliance_intention ~
    descriptive_norm +
    injunctive_norm +
    empirical_expectation +
    normative_expectation +
    personal_attitude +
    norm_salience +
    sanction_salience +
    reference_group_identification +
    institutional_legitimacy +
    trust_in_institution +
    pluralistic_ignorance +
    dynamic_norm_trend +
    condition +
    policy_domain +
    message_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

contribution_model <- lmer(
  contribution_amount ~
    norm_strength_index +
    enforcement_index +
    legitimacy_trust_index +
    reference_group_identification +
    personal_attitude +
    pluralistic_ignorance +
    dynamic_norm_trend +
    complied +
    condition +
    policy_domain +
    message_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

reporting_model <- glmer(
  reported_violation ~
    injunctive_norm +
    normative_expectation +
    sanction_salience +
    sanction_severity +
    institutional_legitimacy +
    reference_group_identification +
    pluralistic_ignorance +
    condition +
    policy_domain +
    message_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

response_time_model <- lmer(
  log_response_time ~
    norm_strength_index +
    norm_salience +
    pluralistic_ignorance +
    legitimacy_trust_index +
    tipping_margin +
    complied +
    condition +
    policy_domain +
    message_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    compliance_model = summary(compliance_model),
    intention_model = summary(intention_model),
    contribution_model = summary(contribution_model),
    reporting_model = summary(reporting_model),
    response_time_model = summary(response_time_model),
    message_effects = emmeans(compliance_model, ~ message_type, type = "response"),
    diagnostics = check_model(contribution_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(compliance_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_compliance_coefficients.csv"))
write_csv(tidy(intention_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_intention_coefficients.csv"))
write_csv(tidy(contribution_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_contribution_coefficients.csv"))
write_csv(tidy(reporting_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_reporting_coefficients.csv"))

message_summary <- dat %>%
  group_by(message_type) %>%
  summarise(
    n = n(),
    compliance_rate = mean(complied, na.rm = TRUE),
    reporting_rate = mean(reported_violation, na.rm = TRUE),
    mean_intention = mean(compliance_intention, na.rm = TRUE),
    mean_post_norm = mean(post_message_norm_perception, na.rm = TRUE),
    mean_contribution = mean(contribution_amount, na.rm = TRUE),
    mean_tipping_margin = mean(tipping_margin, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(message_summary, file.path(output_dir, "r_summary_by_message_type.csv"))

p <- ggplot(message_summary, aes(x = message_type, y = compliance_rate, group = 1)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Compliance rate by norm-message type",
    x = "Message type",
    y = "Compliance rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_compliance_by_message_type_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
