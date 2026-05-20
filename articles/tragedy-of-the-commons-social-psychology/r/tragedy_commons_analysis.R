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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/tragedy_commons_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    group_id = factor(group_id),
    site_id = factor(site_id),
    condition = factor(condition),
    property_regime = factor(property_regime),
    expected_sanction = monitoring_credibility *
      sanction_probability *
      sanction_severity / 10,
    institutional_effectiveness = boundary_clarity *
      monitoring_credibility *
      pmax(sanction_probability, 0.01) *
      pmax(sanction_severity, 0.01) *
      (legitimacy_score / 10) *
      (rule_participation / 10),
    restraint_index = (
      trust_score +
      legitimacy_score +
      reciprocity_expectation +
      stewardship_norm_salience +
      local_ecological_knowledge -
      asymmetry_index
    ) / 5,
    group_size_estimate = n(),
    .by = c(group_id, round)
  ) %>%
  mutate(
    over_extraction = as.integer(
      extraction > sustainable_threshold / group_size_estimate
    ),
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, property_regime, round) %>%
  summarise(
    n = n(),
    groups = n_distinct(group_id),
    mean_extraction = mean(extraction, na.rm = TRUE),
    total_extraction = sum(extraction, na.rm = TRUE),
    mean_stock = mean(resource_stock, na.rm = TRUE),
    mean_regeneration = mean(regeneration, na.rm = TRUE),
    mean_depletion_risk = mean(depletion_risk, na.rm = TRUE),
    over_extraction_rate = mean(over_extraction, na.rm = TRUE),
    mean_trust = mean(trust_score, na.rm = TRUE),
    mean_legitimacy = mean(legitimacy_score, na.rm = TRUE),
    mean_monitoring = mean(monitoring_credibility, na.rm = TRUE),
    mean_institutional_effectiveness =
      mean(institutional_effectiveness, na.rm = TRUE),
    mean_group_welfare = mean(group_welfare, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_regime_round.csv"))

extraction_model <- lmer(
  extraction ~
    round +
    trust_score +
    legitimacy_score +
    monitoring_credibility +
    expected_sanction +
    boundary_clarity +
    rule_participation +
    conflict_resolution_access +
    local_ecological_knowledge +
    perceived_fairness +
    reciprocity_expectation +
    stewardship_norm_salience +
    asymmetry_index +
    resource_stock +
    condition +
    property_regime +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

stock_model <- lmer(
  resource_stock ~
    round +
    extraction +
    regeneration +
    institutional_effectiveness +
    trust_score +
    legitimacy_score +
    monitoring_credibility +
    condition +
    property_regime +
    (1 | group_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

depletion_model <- glmer(
  over_extraction ~
    trust_score +
    legitimacy_score +
    monitoring_credibility +
    expected_sanction +
    boundary_clarity +
    rule_participation +
    stewardship_norm_salience +
    asymmetry_index +
    condition +
    property_regime +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

payoff_model <- lmer(
  individual_payoff ~
    extraction +
    depletion_risk +
    expected_sanction +
    legitimacy_score +
    perceived_fairness +
    condition +
    property_regime +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    round +
    extraction +
    trust_score +
    legitimacy_score +
    monitoring_credibility +
    depletion_risk +
    condition +
    property_regime +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    extraction_model = summary(extraction_model),
    stock_model = summary(stock_model),
    depletion_model = summary(depletion_model),
    payoff_model = summary(payoff_model),
    response_time_model = summary(rt_model),
    extraction_by_condition = emmeans(extraction_model, ~ condition),
    diagnostics = check_model(extraction_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(extraction_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_extraction_coefficients.csv"))
write_csv(tidy(stock_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_stock_coefficients.csv"))
write_csv(tidy(depletion_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_depletion_coefficients.csv"))
write_csv(tidy(payoff_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_payoff_coefficients.csv"))

p <- ggplot(summary_table, aes(x = round, y = mean_stock, color = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Resource stock across repeated commons rounds",
    x = "Round",
    y = "Mean resource stock"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_resource_stock_by_round_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
