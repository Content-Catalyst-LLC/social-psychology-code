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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/collective_action_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    group_id = factor(group_id),
    condition = factor(condition),
    movement_domain = factor(movement_domain),
    recruitment_source = factor(recruitment_source),
    institutional_response = factor(institutional_response),
    action_participation = as.integer(action_participation),
    log_response_time = log(response_time_ms)
  )

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    groups = n_distinct(group_id),
    participation_rate = mean(action_participation, na.rm = TRUE),
    mean_intention = mean(participation_intention, na.rm = TRUE),
    mean_identity = mean(identity_strength, na.rm = TRUE),
    mean_injustice = mean(perceived_injustice, na.rm = TRUE),
    mean_outrage = mean(moral_outrage, na.rm = TRUE),
    mean_efficacy = mean(collective_efficacy, na.rm = TRUE),
    mean_network_support = mean(network_support, na.rm = TRUE),
    mean_cost = mean(participation_cost, na.rm = TRUE),
    mean_repression_risk = mean(perceived_repression_risk, na.rm = TRUE),
    mean_digital_engagement = mean(digital_engagement, na.rm = TRUE),
    mean_offline_engagement = mean(offline_engagement, na.rm = TRUE),
    mean_outcome = mean(movement_outcome, na.rm = TRUE),
    mean_response_time_ms = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_summary_by_condition.csv"))

participation_model <- glmer(
  action_participation ~
    condition +
    movement_domain +
    identity_strength +
    perceived_injustice +
    moral_outrage +
    collective_efficacy +
    network_support +
    mobilization_exposure +
    participation_cost +
    perceived_repression_risk +
    free_rider_incentive +
    perceived_legitimacy +
    (1 | participant) +
    (1 | group_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

intention_model <- lmer(
  participation_intention ~
    condition +
    movement_domain +
    identity_strength +
    perceived_injustice +
    moral_outrage +
    collective_efficacy +
    network_support +
    mobilization_exposure +
    participation_cost +
    perceived_repression_risk +
    free_rider_incentive +
    (1 | participant) +
    (1 | group_id),
  data = dat,
  REML = FALSE
)

digital_model <- lmer(
  digital_engagement ~
    condition +
    movement_domain +
    participation_intention +
    identity_strength +
    network_support +
    mobilization_exposure +
    participation_cost +
    perceived_repression_risk +
    (1 | participant) +
    (1 | group_id),
  data = dat,
  REML = FALSE
)

offline_model <- lmer(
  offline_engagement ~
    condition +
    movement_domain +
    participation_intention +
    identity_strength +
    network_support +
    collective_efficacy +
    participation_cost +
    perceived_repression_risk +
    (1 | participant) +
    (1 | group_id),
  data = dat,
  REML = FALSE
)

outcome_model <- lmer(
  movement_outcome ~
    condition +
    action_participation +
    collective_efficacy +
    network_support +
    digital_engagement +
    offline_engagement +
    perceived_repression_risk +
    perceived_legitimacy +
    (1 | group_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    condition +
    participation_intention +
    identity_strength +
    perceived_injustice +
    collective_efficacy +
    participation_cost +
    perceived_repression_risk +
    free_rider_incentive +
    (1 | participant) +
    (1 | group_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    participation_model = summary(participation_model),
    intention_model = summary(intention_model),
    digital_engagement_model = summary(digital_model),
    offline_engagement_model = summary(offline_model),
    movement_outcome_model = summary(outcome_model),
    response_time_model = summary(rt_model),
    participation_by_condition = emmeans(participation_model, ~ condition, type = "response"),
    model_diagnostics = check_model(participation_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(participation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_participation_coefficients.csv"))
write_csv(tidy(intention_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_intention_coefficients.csv"))
write_csv(tidy(digital_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_digital_engagement_coefficients.csv"))
write_csv(tidy(offline_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_offline_engagement_coefficients.csv"))
write_csv(tidy(outcome_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_movement_outcome_coefficients.csv"))
write_csv(tidy(rt_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_response_time_coefficients.csv"))

domain_summary <- dat %>%
  group_by(movement_domain) %>%
  summarise(
    n = n(),
    participation_rate = mean(action_participation),
    mean_intention = mean(participation_intention),
    mean_identity = mean(identity_strength),
    mean_injustice = mean(perceived_injustice),
    mean_efficacy = mean(collective_efficacy),
    mean_repression_risk = mean(perceived_repression_risk),
    .groups = "drop"
  )

write_csv(domain_summary, file.path(output_dir, "r_summary_by_domain.csv"))

p <- ggplot(dat, aes(x = identity_strength, y = participation_intention, color = condition)) +
  geom_point(alpha = 0.35) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Identity strength and collective action intention",
    x = "Identity strength",
    y = "Participation intention"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_identity_intention_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
