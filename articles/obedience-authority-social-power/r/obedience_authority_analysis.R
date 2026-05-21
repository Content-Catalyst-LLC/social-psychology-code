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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/obedience_trials.csv")
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
    obeyed = as.integer(obeyed),
    resisted = as.integer(resisted),
    protested = as.integer(protest),
    log_response_time = log(response_time_ms),
    authority_pressure_index = (
      authority_legitimacy +
      authority_proximity +
      institutional_prestige +
      command_clarity +
      cost_of_defiance +
      peer_compliance -
      peer_dissent
    ) / 6,
    moral_resistance_index = (
      moral_conflict +
      victim_proximity +
      harm_salience +
      peer_dissent +
      perceived_responsibility_after
    ) / 5,
    identification_index = (
      role_identification +
      mission_identification +
      institutional_prestige
    ) / 3
  )

summary_table <- dat %>%
  group_by(condition, escalation_step) %>%
  summarise(
    n = n(),
    obedience_rate = mean(obeyed, na.rm = TRUE),
    resistance_rate = mean(resisted, na.rm = TRUE),
    protest_rate = mean(protested, na.rm = TRUE),
    mean_hesitation = mean(hesitation, na.rm = TRUE),
    mean_authority_pressure = mean(authority_pressure_index, na.rm = TRUE),
    mean_moral_resistance = mean(moral_resistance_index, na.rm = TRUE),
    mean_identification = mean(identification_index, na.rm = TRUE),
    mean_responsibility_after = mean(perceived_responsibility_after, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_obedience_escalation_summary.csv"))

obedience_model <- glmer(
  obeyed ~
    authority_legitimacy +
    authority_proximity +
    institutional_prestige +
    command_clarity +
    cost_of_defiance +
    escalation_step +
    responsibility_displacement +
    moral_conflict +
    victim_proximity +
    harm_salience +
    peer_dissent +
    peer_compliance +
    role_identification +
    mission_identification +
    condition +
    institution_context +
    (1 + escalation_step | participant),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

resistance_model <- glmer(
  resisted ~
    authority_pressure_index +
    moral_resistance_index +
    identification_index +
    peer_dissent +
    victim_proximity +
    perceived_responsibility_after +
    cost_of_defiance +
    condition +
    institution_context +
    (1 | participant),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

protest_model <- glmer(
  protested ~
    moral_conflict +
    harm_salience +
    peer_dissent +
    responsibility_displacement +
    authority_pressure_index +
    condition +
    institution_context +
    (1 | participant),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

response_time_model <- lmer(
  log_response_time ~
    authority_pressure_index +
    moral_resistance_index +
    responsibility_displacement +
    escalation_step +
    peer_dissent +
    hesitation +
    condition +
    institution_context +
    (1 | participant),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    obedience_model = summary(obedience_model),
    resistance_model = summary(resistance_model),
    protest_model = summary(protest_model),
    response_time_model = summary(response_time_model),
    condition_obedience = emmeans(obedience_model, ~ condition, type = "response"),
    diagnostics = check_model(response_time_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(obedience_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_obedience_coefficients.csv"))
write_csv(tidy(resistance_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_resistance_coefficients.csv"))
write_csv(tidy(response_time_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_response_time_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    obedience_rate = mean(obeyed, na.rm = TRUE),
    resistance_rate = mean(resisted, na.rm = TRUE),
    protest_rate = mean(protested, na.rm = TRUE),
    mean_hesitation = mean(hesitation, na.rm = TRUE),
    mean_authority_pressure = mean(authority_pressure_index, na.rm = TRUE),
    mean_moral_resistance = mean(moral_resistance_index, na.rm = TRUE),
    mean_identification = mean(identification_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_condition_summary.csv"))

p <- ggplot(summary_table, aes(x = escalation_step, y = obedience_rate, color = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Obedience across escalation steps",
    x = "Escalation step",
    y = "Obedience rate"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_obedience_by_escalation_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
