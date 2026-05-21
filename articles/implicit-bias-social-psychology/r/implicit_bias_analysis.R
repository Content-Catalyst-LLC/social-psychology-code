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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/implicit_bias_trials.csv")
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
    condition = factor(condition),
    congruent_block = as.integer(congruent_block),
    accuracy = as.integer(accuracy),
    log_response_time = log(response_time_ms),
    automaticity_risk_index = (
      cognitive_load +
      time_pressure -
      accountability -
      structured_decision_support
    ) / 4,
    mitigation_index = (
      accountability +
      counter_stereotypical_exposure +
      perspective_taking +
      structured_decision_support
    ) / 4
  )

rt_dat <- dat %>%
  filter(response_time_ms >= 250, accuracy == 1)

d_scores <- rt_dat %>%
  group_by(participant, condition, congruent_block) %>%
  summarise(mean_rt = mean(response_time_ms, na.rm = TRUE), .groups = "drop") %>%
  pivot_wider(names_from = congruent_block, values_from = mean_rt, names_prefix = "block_") %>%
  left_join(
    rt_dat %>%
      group_by(participant, condition) %>%
      summarise(pooled_sd = sd(response_time_ms, na.rm = TRUE), .groups = "drop"),
    by = c("participant", "condition")
  ) %>%
  mutate(d_score = (block_0 - block_1) / pooled_sd)

write_csv(d_scores, file.path(output_dir, "r_participant_d_scores.csv"))

summary_table <- dat %>%
  group_by(condition, institution_context) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_rt = mean(response_time_ms, na.rm = TRUE),
    accuracy_rate = mean(accuracy, na.rm = TRUE),
    mean_explicit_attitude = mean(explicit_attitude, na.rm = TRUE),
    mean_judgment = mean(judgment_score, na.rm = TRUE),
    mean_behavioral_outcome = mean(behavioral_outcome, na.rm = TRUE),
    mean_automaticity_risk = mean(automaticity_risk_index, na.rm = TRUE),
    mean_mitigation = mean(mitigation_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

latency_model <- lmer(
  log_response_time ~
    congruent_block +
    explicit_attitude +
    cognitive_load +
    accountability +
    time_pressure +
    counter_stereotypical_exposure +
    perspective_taking +
    structured_decision_support +
    condition +
    institution_context +
    (1 + congruent_block | participant) +
    (1 | scenario_id),
  data = rt_dat,
  REML = FALSE
)

judgment_model <- lmer(
  judgment_score ~
    congruent_block +
    explicit_attitude +
    automaticity_risk_index +
    mitigation_index +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

behavior_model <- lmer(
  behavioral_outcome ~
    congruent_block +
    explicit_attitude +
    judgment_score +
    automaticity_risk_index +
    mitigation_index +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

accuracy_model <- glmer(
  accuracy ~
    congruent_block +
    cognitive_load +
    time_pressure +
    accountability +
    structured_decision_support +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

capture.output(
  list(
    latency_model = summary(latency_model),
    judgment_model = summary(judgment_model),
    behavior_model = summary(behavior_model),
    accuracy_model = summary(accuracy_model),
    congruent_block_latency = emmeans(latency_model, ~ congruent_block),
    diagnostics = check_model(judgment_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(latency_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_latency_coefficients.csv"))
write_csv(tidy(judgment_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_judgment_coefficients.csv"))
write_csv(tidy(behavior_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_behavior_coefficients.csv"))

d_summary <- d_scores %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_d_score = mean(d_score, na.rm = TRUE),
    sd_d_score = sd(d_score, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(d_summary, file.path(output_dir, "r_d_score_summary_by_condition.csv"))

p <- ggplot(d_summary, aes(x = reorder(condition, mean_d_score), y = mean_d_score, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean implicit-association D-score by condition",
    x = "Condition",
    y = "Mean D-score"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_d_score_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
