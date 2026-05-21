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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/conformity_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    group_id = factor(group_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    context = factor(context),
    condition = factor(condition),
    conformed = as.integer(conformed),
    dissented = as.integer(dissented),
    confidence_shift = confidence_post - confidence_pre,
    normative_influence_index = (
      normative_pressure +
      unanimity +
      cohesion +
      status_strength +
      public_response * 10 +
      group_identification -
      visible_dissent
    ) / 6,
    informational_influence_index = (
      ambiguity +
      informational_uncertainty +
      status_strength +
      social_proof_metrics -
      visible_dissent
    ) / 4,
    digital_social_proof_index = (
      network_exposure +
      social_proof_metrics +
      algorithmic_amplification
    ) / 3,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, context) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    groups = n_distinct(group_id),
    conformity_rate = mean(conformed, na.rm = TRUE),
    dissent_rate = mean(dissented, na.rm = TRUE),
    mean_confidence_shift = mean(confidence_shift, na.rm = TRUE),
    mean_normative_influence = mean(normative_influence_index, na.rm = TRUE),
    mean_informational_influence = mean(informational_influence_index, na.rm = TRUE),
    mean_digital_social_proof = mean(digital_social_proof_index, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

conformity_model <- glmer(
  conformed ~
    ambiguity +
    majority_size +
    unanimity +
    visible_dissent +
    cohesion +
    normative_pressure +
    informational_uncertainty +
    status_strength +
    public_response +
    private_response +
    group_identification +
    social_identity_salience +
    minority_consistency +
    network_exposure +
    social_proof_metrics +
    algorithmic_amplification +
    condition +
    context +
    (1 + ambiguity | participant) +
    (1 | group_id) +
    (1 | scenario_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

dissent_model <- glmer(
  dissented ~
    visible_dissent +
    minority_consistency +
    private_response +
    normative_pressure +
    unanimity +
    cohesion +
    public_response +
    condition +
    context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

confidence_model <- lmer(
  confidence_shift ~
    ambiguity +
    informational_uncertainty +
    status_strength +
    unanimity +
    visible_dissent +
    social_proof_metrics +
    algorithmic_amplification +
    condition +
    context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    ambiguity +
    unanimity +
    visible_dissent +
    normative_pressure +
    informational_uncertainty +
    conformed +
    condition +
    context +
    (1 | participant) +
    (1 | group_id) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    conformity_model = summary(conformity_model),
    dissent_model = summary(dissent_model),
    confidence_model = summary(confidence_model),
    response_time_model = summary(response_time_model),
    condition_conformity = emmeans(conformity_model, ~ condition, type = "response"),
    diagnostics = check_model(response_time_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(conformity_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_conformity_coefficients.csv"))
write_csv(tidy(dissent_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_dissent_coefficients.csv"))
write_csv(tidy(confidence_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_confidence_shift_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    conformity_rate = mean(conformed, na.rm = TRUE),
    dissent_rate = mean(dissented, na.rm = TRUE),
    mean_visible_dissent = mean(visible_dissent, na.rm = TRUE),
    mean_unanimity = mean(unanimity, na.rm = TRUE),
    mean_confidence_shift = mean(confidence_shift, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_summary_by_condition.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, conformity_rate), y = conformity_rate, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Conformity rate by condition",
    x = "Condition",
    y = "Conformity rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_conformity_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
