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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/diffusion_responsibility_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    scenario_domain = factor(scenario_domain),
    intervention_decision = as.integer(intervention_decision),
    reporting_decision = as.integer(reporting_decision),
    pluralistic_ignorance_gap = private_concern - perceived_group_concern,
    diffusion_pressure = log1p(bystander_count) +
      0.30 * organizational_fragmentation +
      0.20 * ambiguity_level,
    responsibility_clarity_index = (
      role_clarity + accountability_assignment + leadership_cue
    ) / 3,
    log_delay = log1p(intervention_delay_seconds),
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, scenario_domain) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_bystanders = mean(bystander_count, na.rm = TRUE),
    intervention_rate = mean(intervention_decision, na.rm = TRUE),
    reporting_rate = mean(reporting_decision, na.rm = TRUE),
    mean_delay = mean(intervention_delay_seconds, na.rm = TRUE),
    mean_responsibility = mean(perceived_responsibility, na.rm = TRUE),
    mean_role_clarity = mean(role_clarity, na.rm = TRUE),
    mean_ambiguity = mean(ambiguity_level, na.rm = TRUE),
    mean_evaluation = mean(evaluation_apprehension, na.rm = TRUE),
    mean_pluralistic_gap = mean(pluralistic_ignorance_gap, na.rm = TRUE),
    mean_diffusion_pressure = mean(diffusion_pressure, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_domain.csv"))

intervention_model <- glmer(
  intervention_decision ~
    bystander_count +
    ambiguity_level +
    evaluation_apprehension +
    private_concern +
    perceived_responsibility +
    role_clarity +
    intervention_efficacy +
    accountability_assignment +
    leadership_cue +
    organizational_fragmentation +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

reporting_model <- glmer(
  reporting_decision ~
    bystander_count +
    ambiguity_level +
    evaluation_apprehension +
    private_concern +
    perceived_responsibility +
    role_clarity +
    accountability_assignment +
    leadership_cue +
    organizational_fragmentation +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

responsibility_model <- lmer(
  perceived_responsibility ~
    bystander_count +
    ambiguity_level +
    evaluation_apprehension +
    role_clarity +
    accountability_assignment +
    leadership_cue +
    social_visibility +
    organizational_fragmentation +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

delay_model <- lmer(
  log_delay ~
    bystander_count +
    ambiguity_level +
    evaluation_apprehension +
    perceived_responsibility +
    role_clarity +
    intervention_efficacy +
    organizational_fragmentation +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

pluralistic_model <- lmer(
  pluralistic_ignorance_gap ~
    bystander_count +
    ambiguity_level +
    evaluation_apprehension +
    leadership_cue +
    role_clarity +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    bystander_count +
    ambiguity_level +
    evaluation_apprehension +
    perceived_responsibility +
    role_clarity +
    diffusion_pressure +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

bystander_summary <- dat %>%
  mutate(
    bystander_band = case_when(
      bystander_count == 0 ~ "alone",
      bystander_count <= 2 ~ "small",
      bystander_count <= 6 ~ "medium",
      TRUE ~ "large"
    )
  ) %>%
  group_by(bystander_band) %>%
  summarise(
    n = n(),
    intervention_rate = mean(intervention_decision, na.rm = TRUE),
    reporting_rate = mean(reporting_decision, na.rm = TRUE),
    mean_responsibility = mean(perceived_responsibility, na.rm = TRUE),
    mean_delay = mean(intervention_delay_seconds, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(bystander_summary, file.path(output_dir, "r_bystander_summary.csv"))

capture.output(
  list(
    intervention_model = summary(intervention_model),
    reporting_model = summary(reporting_model),
    responsibility_model = summary(responsibility_model),
    delay_model = summary(delay_model),
    pluralistic_model = summary(pluralistic_model),
    response_time_model = summary(rt_model),
    intervention_by_condition = emmeans(intervention_model, ~ condition, type = "response"),
    diagnostics = check_model(responsibility_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(intervention_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_intervention_coefficients.csv"))
write_csv(tidy(reporting_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_reporting_coefficients.csv"))
write_csv(tidy(responsibility_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_responsibility_coefficients.csv"))
write_csv(tidy(delay_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_delay_coefficients.csv"))
write_csv(tidy(pluralistic_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_pluralistic_gap_coefficients.csv"))

p <- ggplot(dat, aes(x = bystander_count, y = perceived_responsibility, color = condition)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Bystander count and perceived responsibility",
    x = "Bystander count",
    y = "Perceived personal responsibility"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_bystander_responsibility_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
