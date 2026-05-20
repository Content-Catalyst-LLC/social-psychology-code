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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/social_facilitation_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    site_id = factor(site_id),
    condition = factor(condition),
    task_domain = factor(task_domain),
    audience_present = as.integer(audience_present),
    coaction_present = as.integer(coaction_present),
    digital_monitoring = as.integer(digital_monitoring),
    dominant_response_correct = as.integer(dominant_response_correct),
    social_presence_intensity = audience_present +
      0.65 * coaction_present +
      0.50 * digital_monitoring,
    mastery_advantage = task_mastery - task_difficulty,
    simple_or_mastered = as.integer(mastery_advantage >= 1.0),
    complex_or_unmastered = as.integer(mastery_advantage < 0.0),
    evaluation_apprehension_index = (
      evaluation_pressure +
      perceived_scrutiny +
      observer_expertise +
      social_anxiety
    ) / 4,
    distraction_conflict_index = (
      distraction_index +
      attentional_conflict +
      perceived_scrutiny
    ) / 3,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, task_domain) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_performance = mean(performance_score, na.rm = TRUE),
    mean_accuracy = mean(accuracy, na.rm = TRUE),
    mean_error_rate = mean(error_rate, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    mean_arousal = mean(arousal_index, na.rm = TRUE),
    mean_distraction = mean(distraction_index, na.rm = TRUE),
    mean_evaluation = mean(evaluation_pressure, na.rm = TRUE),
    mean_task_difficulty = mean(task_difficulty, na.rm = TRUE),
    mean_task_mastery = mean(task_mastery, na.rm = TRUE),
    mean_social_presence = mean(social_presence_intensity, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_domain.csv"))

performance_model <- lmer(
  performance_score ~
    social_presence_intensity * task_difficulty +
    social_presence_intensity * task_mastery +
    evaluation_pressure +
    perceived_scrutiny +
    arousal_index +
    distraction_conflict_index +
    dominant_response_correct +
    baseline_skill +
    audience_valence +
    condition +
    task_domain +
    (1 + social_presence_intensity | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

accuracy_model <- lmer(
  accuracy ~
    social_presence_intensity * task_difficulty +
    social_presence_intensity * task_mastery +
    evaluation_pressure +
    arousal_index +
    attentional_conflict +
    dominant_response_correct +
    baseline_skill +
    condition +
    task_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

error_model <- lmer(
  error_rate ~
    social_presence_intensity * task_difficulty +
    evaluation_pressure +
    arousal_index +
    distraction_conflict_index +
    dominant_response_correct +
    task_mastery +
    social_anxiety +
    condition +
    task_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

arousal_model <- lmer(
  arousal_index ~
    audience_present +
    coaction_present +
    digital_monitoring +
    evaluation_pressure +
    perceived_scrutiny +
    observer_expertise +
    audience_size +
    audience_valence +
    social_anxiety +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    social_presence_intensity * task_difficulty +
    task_mastery +
    evaluation_pressure +
    perceived_scrutiny +
    attentional_conflict +
    arousal_index +
    condition +
    task_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    performance_model = summary(performance_model),
    accuracy_model = summary(accuracy_model),
    error_model = summary(error_model),
    arousal_model = summary(arousal_model),
    response_time_model = summary(rt_model),
    audience_by_difficulty = emmeans(performance_model, ~ social_presence_intensity | task_difficulty),
    diagnostics = check_model(performance_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(performance_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_performance_coefficients.csv"))
write_csv(tidy(accuracy_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_accuracy_coefficients.csv"))
write_csv(tidy(error_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_error_coefficients.csv"))
write_csv(tidy(arousal_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_arousal_coefficients.csv"))

difficulty_summary <- dat %>%
  mutate(
    difficulty_band = cut(
      task_difficulty,
      breaks = c(-0.1, 3.33, 6.66, 10.1),
      labels = c("low", "medium", "high")
    )
  ) %>%
  group_by(condition, difficulty_band) %>%
  summarise(
    n = n(),
    mean_performance = mean(performance_score, na.rm = TRUE),
    mean_accuracy = mean(accuracy, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(difficulty_summary, file.path(output_dir, "r_summary_by_condition_difficulty.csv"))

p <- ggplot(difficulty_summary, aes(x = difficulty_band, y = mean_performance, color = condition, group = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Social facilitation by task difficulty",
    x = "Task difficulty band",
    y = "Mean performance score"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_performance_by_difficulty_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
