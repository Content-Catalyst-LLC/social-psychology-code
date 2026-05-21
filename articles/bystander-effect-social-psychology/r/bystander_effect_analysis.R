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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/bystander_effect_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    condition = factor(condition),
    context_type = factor(context_type),
    direct_assignment = as.integer(direct_assignment),
    leadership_cue = as.integer(leadership_cue),
    online_context = as.integer(online_context),
    actual_intervention = as.integer(actual_intervention),
    log_perceived_bystanders = log1p(perceived_bystander_count),
    responsibility_assignment_index = (
      felt_responsibility +
      2 * direct_assignment +
      1.4 * leadership_cue +
      intervention_norm_salience
    ) / 4,
    ambiguity_index = (
      pluralistic_ignorance +
      evaluation_apprehension +
      (10 - emergency_clarity)
    ) / 3,
    helping_capacity_index = (
      perceived_competence +
      response_confidence +
      intervention_norm_salience -
      intervention_cost
    ) / 3,
    log_latency = log(intervention_latency_ms)
  )

summary_table <- dat %>%
  group_by(condition, context_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_perceived_bystanders = mean(perceived_bystander_count, na.rm = TRUE),
    intervention_rate = mean(actual_intervention, na.rm = TRUE),
    mean_intervention_likelihood = mean(intervention_likelihood, na.rm = TRUE),
    mean_latency = mean(intervention_latency_ms, na.rm = TRUE),
    mean_responsibility = mean(felt_responsibility, na.rm = TRUE),
    mean_diffusion = mean(diffusion_responsibility, na.rm = TRUE),
    mean_pluralistic_ignorance = mean(pluralistic_ignorance, na.rm = TRUE),
    mean_evaluation_apprehension = mean(evaluation_apprehension, na.rm = TRUE),
    mean_clarity = mean(emergency_clarity, na.rm = TRUE),
    mean_competence = mean(perceived_competence, na.rm = TRUE),
    mean_assignment_index = mean(responsibility_assignment_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

intervention_model <- glmer(
  actual_intervention ~
    log_perceived_bystanders +
    emergency_clarity +
    danger_level +
    victim_identifiability +
    shared_identity +
    felt_responsibility +
    diffusion_responsibility +
    pluralistic_ignorance +
    evaluation_apprehension +
    perceived_competence +
    intervention_cost +
    direct_assignment +
    leadership_cue +
    intervention_norm_salience +
    online_context +
    platform_traceability +
    moderation_visibility +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

likelihood_model <- lmer(
  intervention_likelihood ~
    log_perceived_bystanders +
    emergency_clarity +
    danger_level +
    victim_identifiability +
    shared_identity +
    felt_responsibility +
    diffusion_responsibility +
    pluralistic_ignorance +
    evaluation_apprehension +
    perceived_competence +
    intervention_cost +
    direct_assignment +
    leadership_cue +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

responsibility_model <- lmer(
  felt_responsibility ~
    log_perceived_bystanders +
    direct_assignment +
    leadership_cue +
    shared_identity +
    victim_identifiability +
    emergency_clarity +
    intervention_norm_salience +
    diffusion_responsibility +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

latency_model <- lmer(
  log_latency ~
    log_perceived_bystanders +
    emergency_clarity +
    pluralistic_ignorance +
    evaluation_apprehension +
    intervention_cost +
    direct_assignment +
    leadership_cue +
    perceived_competence +
    actual_intervention +
    condition +
    context_type +
    (1 | participant) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat %>% filter(intervention_latency_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    intervention_model = summary(intervention_model),
    likelihood_model = summary(likelihood_model),
    responsibility_model = summary(responsibility_model),
    latency_model = summary(latency_model),
    condition_intervention_rates = emmeans(intervention_model, ~ condition, type = "response"),
    diagnostics = check_model(likelihood_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(intervention_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_intervention_coefficients.csv"))
write_csv(tidy(likelihood_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_likelihood_coefficients.csv"))
write_csv(tidy(responsibility_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_responsibility_coefficients.csv"))
write_csv(tidy(latency_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_latency_coefficients.csv"))

bystander_summary <- dat %>%
  mutate(
    bystander_band = cut(
      perceived_bystander_count,
      breaks = c(-0.1, 0, 3, 10, 10000),
      labels = c("alone", "small_group", "medium_group", "large_group")
    )
  ) %>%
  group_by(condition, bystander_band) %>%
  summarise(
    n = n(),
    intervention_rate = mean(actual_intervention, na.rm = TRUE),
    mean_likelihood = mean(intervention_likelihood, na.rm = TRUE),
    mean_latency = mean(intervention_latency_ms, na.rm = TRUE),
    mean_responsibility = mean(felt_responsibility, na.rm = TRUE),
    mean_diffusion = mean(diffusion_responsibility, na.rm = TRUE),
    mean_ambiguity = mean(ambiguity_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(bystander_summary, file.path(output_dir, "r_summary_by_condition_bystander_band.csv"))

p <- ggplot(bystander_summary, aes(x = bystander_band, y = intervention_rate, color = condition, group = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Bystander intervention by perceived group size",
    x = "Perceived bystander-count band",
    y = "Intervention rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_intervention_by_bystander_band_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
