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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/stereotypes_prejudice_trials.csv")
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
    target_group = factor(target_group),
    evaluator_group = factor(evaluator_group),
    log_response_time = log(response_time_ms),
    contact_support_index = (
      contact_quality + contact_quantity + institutional_support
    ) / 3,
    threat_competition_index = (
      perceived_threat + perceived_competition
    ) / 2,
    decision_structure_index = (
      structured_criteria + accountability
    ) / 2,
    stereotype_content_asymmetry = competence_rating - warmth_rating
  )

summary_table <- dat %>%
  group_by(condition, institution_context) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_stereotype_strength = mean(stereotype_strength, na.rm = TRUE),
    mean_prejudice = mean(prejudice_rating, na.rm = TRUE),
    mean_discrimination = mean(discrimination_tendency, na.rm = TRUE),
    mean_behavioral_outcome = mean(behavioral_outcome, na.rm = TRUE),
    mean_performance = mean(performance_score, na.rm = TRUE),
    mean_contact_support = mean(contact_support_index, na.rm = TRUE),
    mean_threat_competition = mean(threat_competition_index, na.rm = TRUE),
    mean_decision_structure = mean(decision_structure_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

prejudice_model <- lmer(
  prejudice_rating ~
    stereotype_strength +
    perceived_threat +
    perceived_competition +
    contact_quality +
    contact_quantity +
    institutional_support +
    implicit_score +
    explicit_attitude +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

discrimination_model <- lmer(
  discrimination_tendency ~
    stereotype_strength +
    prejudice_rating +
    perceived_threat +
    implicit_score +
    explicit_attitude +
    structured_criteria +
    accountability +
    institutional_support +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

performance_model <- lmer(
  performance_score ~
    stereotype_threat_salience +
    identity_safety +
    institutional_support +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

warmth_model <- lmer(
  warmth_rating ~
    perceived_competition +
    perceived_threat +
    contact_quality +
    institutional_support +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

competence_model <- lmer(
  competence_rating ~
    perceived_status +
    perceived_competition +
    stereotype_strength +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    stereotype_strength +
    prejudice_rating +
    perceived_threat +
    stereotype_threat_salience +
    structured_criteria +
    condition +
    institution_context +
    (1 | participant) +
    (1 | scenario_id),
  data = dat %>% filter(response_time_ms >= 250),
  REML = FALSE
)

capture.output(
  list(
    prejudice_model = summary(prejudice_model),
    discrimination_model = summary(discrimination_model),
    performance_model = summary(performance_model),
    warmth_model = summary(warmth_model),
    competence_model = summary(competence_model),
    response_time_model = summary(response_time_model),
    condition_prejudice = emmeans(prejudice_model, ~ condition),
    diagnostics = check_model(prejudice_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(prejudice_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_prejudice_coefficients.csv"))
write_csv(tidy(discrimination_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_discrimination_coefficients.csv"))
write_csv(tidy(performance_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_performance_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_prejudice = mean(prejudice_rating, na.rm = TRUE),
    mean_discrimination = mean(discrimination_tendency, na.rm = TRUE),
    mean_contact_support = mean(contact_support_index, na.rm = TRUE),
    mean_threat_competition = mean(threat_competition_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_condition_summary.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_prejudice), y = mean_prejudice, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean prejudice rating by condition",
    x = "Condition",
    y = "Mean prejudice rating"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_prejudice_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
