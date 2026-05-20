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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/social_dilemmas_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    group_id = factor(group_id),
    site_id = factor(site_id),
    condition = factor(condition),
    dilemma_type = factor(dilemma_type),
    free_riding_index = if_else(endowment > 0, (endowment - contribution) / endowment, NA_real_),
    institutional_effectiveness = monitoring_strength *
      sanction_probability *
      sanction_severity *
      (institutional_legitimacy / 10),
    cooperation_score = if_else(dilemma_type == "commons", -extraction, contribution),
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, dilemma_type, round) %>%
  summarise(
    n = n(),
    groups = n_distinct(group_id),
    mean_contribution = mean(contribution, na.rm = TRUE),
    mean_extraction = mean(extraction, na.rm = TRUE),
    mean_free_riding = mean(free_riding_index, na.rm = TRUE),
    mean_trust = mean(trust_score, na.rm = TRUE),
    mean_norm_salience = mean(norm_salience, na.rm = TRUE),
    mean_enforcement = mean(enforcement_signal, na.rm = TRUE),
    mean_legitimacy = mean(institutional_legitimacy, na.rm = TRUE),
    mean_group_welfare = mean(group_welfare, na.rm = TRUE),
    mean_resource_stock = mean(resource_stock, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_type_round.csv"))

public_goods <- dat %>% filter(dilemma_type != "commons")
commons <- dat %>% filter(dilemma_type == "commons")

contribution_model <- lmer(
  contribution ~
    round +
    trust_score +
    norm_salience +
    enforcement_signal +
    fairness_score +
    institutional_legitimacy +
    monitoring_strength +
    sanction_probability +
    sanction_severity +
    reciprocity_expectation +
    condition +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = public_goods,
  REML = FALSE
)

extraction_model <- lmer(
  extraction ~
    round +
    trust_score +
    norm_salience +
    enforcement_signal +
    fairness_score +
    institutional_legitimacy +
    monitoring_strength +
    sanction_probability +
    sanction_severity +
    reciprocity_expectation +
    resource_stock +
    condition +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = commons,
  REML = FALSE
)

payoff_model <- lmer(
  individual_payoff ~
    contribution +
    extraction +
    trust_score +
    norm_salience +
    institutional_legitimacy +
    institutional_effectiveness +
    condition +
    dilemma_type +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

welfare_model <- lmer(
  group_welfare ~
    contribution +
    extraction +
    trust_score +
    norm_salience +
    institutional_legitimacy +
    institutional_effectiveness +
    condition +
    dilemma_type +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    round +
    trust_score +
    norm_salience +
    enforcement_signal +
    fairness_score +
    institutional_legitimacy +
    condition +
    dilemma_type +
    (1 | group_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    contribution_model = summary(contribution_model),
    extraction_model = summary(extraction_model),
    payoff_model = summary(payoff_model),
    welfare_model = summary(welfare_model),
    response_time_model = summary(rt_model),
    contribution_by_condition = emmeans(contribution_model, ~ condition),
    diagnostics = check_model(contribution_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(contribution_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_contribution_coefficients.csv"))
write_csv(tidy(extraction_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_extraction_coefficients.csv"))
write_csv(tidy(payoff_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_payoff_coefficients.csv"))
write_csv(tidy(welfare_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_welfare_coefficients.csv"))

p <- ggplot(summary_table %>% filter(dilemma_type != "commons"), aes(x = round, y = mean_contribution, color = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Public-goods contribution across social dilemma rounds",
    x = "Round",
    y = "Mean contribution"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_contribution_by_round_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
