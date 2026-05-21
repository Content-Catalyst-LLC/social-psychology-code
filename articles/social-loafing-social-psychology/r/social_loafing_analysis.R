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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/social_loafing_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    team_id = factor(team_id),
    site_id = factor(site_id),
    condition = factor(condition),
    task_type = factor(task_type),
    remote_status = factor(remote_status),
    log_group_size = log1p(group_size),
    accountability_index = (identifiability + accountability + task_visibility + evaluation_potential + digital_traceability) / 5,
    collective_effort_index = (perceived_instrumentality + task_value + task_uniqueness + group_identity_salience + group_cohesion - perceived_dispensability) / 5,
    motivation_loss_share = motivation_loss / pmax(coordination_loss + motivation_loss, 0.000001),
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, task_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_group_size = mean(group_size, na.rm = TRUE),
    mean_solo_effort = mean(solo_effort, na.rm = TRUE),
    mean_group_effort = mean(group_effort, na.rm = TRUE),
    mean_effort_loss = mean(effort_loss, na.rm = TRUE),
    mean_motivation_loss = mean(motivation_loss, na.rm = TRUE),
    mean_output = mean(output_score, na.rm = TRUE),
    mean_accountability = mean(accountability_index, na.rm = TRUE),
    mean_collective_effort = mean(collective_effort_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_task.csv"))

effort_loss_model <- lmer(
  effort_loss ~ log_group_size + identifiability + accountability + task_value +
    task_uniqueness + perceived_dispensability + perceived_instrumentality +
    free_rider_expectation + sucker_effect_concern + group_cohesion +
    group_identity_salience + digital_traceability + condition + task_type +
    remote_status + (1 + log_group_size | participant) + (1 | team_id) + (1 | site_id),
  data = dat,
  REML = FALSE
)

motivation_loss_model <- lmer(
  motivation_loss ~ log_group_size + accountability_index + collective_effort_index +
    perceived_dispensability + free_rider_expectation + sucker_effect_concern +
    social_compensation_tendency + condition + task_type + remote_status +
    (1 | participant) + (1 | team_id) + (1 | site_id),
  data = dat,
  REML = FALSE
)

output_model <- lmer(
  output_score ~ group_effort + coordination_loss + motivation_loss +
    accountability_index + collective_effort_index + condition + task_type +
    remote_status + (1 | participant) + (1 | team_id) + (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~ log_group_size + coordination_loss + motivation_loss +
    accountability_index + collective_effort_index + condition + task_type +
    remote_status + (1 | participant) + (1 | team_id) + (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    effort_loss_model = summary(effort_loss_model),
    motivation_loss_model = summary(motivation_loss_model),
    output_model = summary(output_model),
    response_time_model = summary(rt_model),
    condition_means = emmeans(effort_loss_model, ~ condition),
    diagnostics = check_model(effort_loss_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(effort_loss_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_effort_loss_coefficients.csv"))
write_csv(tidy(motivation_loss_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_motivation_loss_coefficients.csv"))
write_csv(tidy(output_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_output_coefficients.csv"))

group_size_summary <- dat %>%
  mutate(group_size_band = cut(group_size, breaks = c(0, 1, 3, 6, 10, 10000), labels = c("solo", "dyad_triads", "small_group", "medium_group", "large_group"))) %>%
  group_by(condition, group_size_band) %>%
  summarise(
    n = n(),
    mean_effort_loss = mean(effort_loss, na.rm = TRUE),
    mean_motivation_loss = mean(motivation_loss, na.rm = TRUE),
    mean_output = mean(output_score, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(group_size_summary, file.path(output_dir, "r_summary_by_condition_group_size.csv"))

p <- ggplot(group_size_summary, aes(x = group_size_band, y = mean_effort_loss, color = condition, group = condition)) +
  geom_line() +
  geom_point() +
  labs(title = "Social loafing by group size and condition", x = "Group size band", y = "Mean effort loss") +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_effort_loss_by_group_size_plot.png"), p, width = 9, height = 6, dpi = 300)
message("R analysis complete. Outputs written to: ", output_dir)
