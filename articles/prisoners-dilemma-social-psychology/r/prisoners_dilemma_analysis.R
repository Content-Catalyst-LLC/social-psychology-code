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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/prisoners_dilemma_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  arrange(dyad_id, participant, round) %>%
  mutate(
    participant = factor(participant),
    dyad_id = factor(dyad_id),
    site_id = factor(site_id),
    condition = factor(condition),
    horizon_type = factor(horizon_type),
    cooperate = as.integer(cooperate),
    partner_cooperate = as.integer(partner_cooperate),
    previous_partner_cooperate = lag(partner_cooperate),
    previous_own_cooperate = lag(cooperate),
    temptation_gap = temptation_payoff - reward_payoff,
    cooperation_surplus = 2 * reward_payoff - (temptation_payoff + sucker_payoff),
    log_response_time = log(response_time_ms),
    .by = c(dyad_id, participant)
  )

summary_table <- dat %>%
  group_by(condition, round) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    dyads = n_distinct(dyad_id),
    cooperation_rate = mean(cooperate, na.rm = TRUE),
    partner_cooperation_rate = mean(partner_cooperate, na.rm = TRUE),
    mean_payoff = mean(own_payoff, na.rm = TRUE),
    mean_cumulative_payoff = mean(cumulative_payoff, na.rm = TRUE),
    mean_trust = mean(trust_score, na.rm = TRUE),
    mean_fairness = mean(fairness_score, na.rm = TRUE),
    mean_expected_partner_cooperation = mean(expected_partner_cooperation, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_round.csv"))

coop_model <- glmer(
  cooperate ~
    round +
    previous_partner_cooperate +
    trust_score +
    fairness_score +
    expected_partner_cooperation +
    communication_access +
    reputation_visibility +
    monitoring_strength +
    institutional_enforcement +
    social_identity_salience +
    temptation_gap +
    condition +
    (1 | dyad_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

payoff_model <- lmer(
  own_payoff ~
    cooperate * partner_cooperate +
    round +
    trust_score +
    fairness_score +
    institutional_enforcement +
    condition +
    (1 | dyad_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

trust_model <- lmer(
  trust_score ~
    previous_partner_cooperate +
    communication_access +
    reputation_visibility +
    institutional_enforcement +
    social_identity_salience +
    condition +
    (1 | dyad_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

fairness_model <- lmer(
  fairness_score ~
    own_payoff +
    partner_cooperate +
    cooperate +
    institutional_enforcement +
    condition +
    (1 | dyad_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    round +
    cooperate +
    partner_cooperate +
    trust_score +
    fairness_score +
    expected_partner_cooperation +
    condition +
    (1 | dyad_id) +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

reciprocity_summary <- dat %>%
  filter(!is.na(previous_partner_cooperate)) %>%
  group_by(condition, previous_partner_cooperate) %>%
  summarise(
    n = n(),
    cooperation_rate = mean(cooperate, na.rm = TRUE),
    mean_trust = mean(trust_score, na.rm = TRUE),
    mean_payoff = mean(own_payoff, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(reciprocity_summary, file.path(output_dir, "r_reciprocity_summary.csv"))

capture.output(
  list(
    cooperation_model = summary(coop_model),
    payoff_model = summary(payoff_model),
    trust_model = summary(trust_model),
    fairness_model = summary(fairness_model),
    response_time_model = summary(rt_model),
    cooperation_by_condition = emmeans(coop_model, ~ condition, type = "response"),
    diagnostics = check_model(payoff_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(coop_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_cooperation_coefficients.csv"))
write_csv(tidy(payoff_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_payoff_coefficients.csv"))
write_csv(tidy(trust_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_trust_coefficients.csv"))
write_csv(tidy(fairness_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_fairness_coefficients.csv"))

p <- ggplot(summary_table, aes(x = round, y = cooperation_rate, color = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Cooperation across repeated prisoner’s dilemma rounds",
    x = "Round",
    y = "Cooperation rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_cooperation_by_round_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
