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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/intergroup_conflict_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    group_id = factor(group_id),
    outgroup_id = factor(outgroup_id),
    dyad_id = factor(dyad_id),
    scenario_id = factor(scenario_id),
    site_id = factor(site_id),
    condition = factor(condition),
    context_type = factor(context_type),
    material_conflict_index = (
      resource_competition +
      zero_sum_perception +
      realistic_threat
    ) / 3,
    identity_threat_index = (
      identity_salience +
      group_identification +
      status_threat +
      symbolic_threat
    ) / 4,
    dehumanization_exclusion_index = (
      stereotype_endorsement +
      dehumanization +
      support_for_exclusion / 10
    ) / 3,
    cooperative_contact_index = (
      contact_quality +
      equal_status +
      common_goal_salience +
      institutional_support
    ) / 4,
    legitimacy_index = (
      perceived_legitimacy +
      institutional_trust
    ) / 2,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, context_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    groups = n_distinct(group_id),
    dyads = n_distinct(dyad_id),
    mean_hostility = mean(hostility_score, na.rm = TRUE),
    mean_aggression = mean(aggression_intention, na.rm = TRUE),
    mean_avoidance = mean(avoidance_intention, na.rm = TRUE),
    mean_exclusion = mean(support_for_exclusion, na.rm = TRUE),
    mean_cooperation = mean(support_for_cooperation, na.rm = TRUE),
    mean_material_conflict = mean(material_conflict_index, na.rm = TRUE),
    mean_identity_threat = mean(identity_threat_index, na.rm = TRUE),
    mean_dehumanization_exclusion = mean(dehumanization_exclusion_index, na.rm = TRUE),
    mean_contact = mean(cooperative_contact_index, na.rm = TRUE),
    mean_legitimacy = mean(legitimacy_index, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

hostility_model <- lmer(
  hostility_score ~
    material_conflict_index +
    identity_threat_index +
    stereotype_endorsement +
    outgroup_warmth +
    outgroup_competence +
    intergroup_anxiety +
    perceived_injustice +
    dehumanization +
    norm_of_retaliation +
    group_polarization +
    cooperative_contact_index +
    legitimacy_index +
    cooperative_task_success +
    condition +
    context_type +
    (1 | participant) +
    (1 | group_id) +
    (1 | outgroup_id) +
    (1 | dyad_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

aggression_model <- lmer(
  aggression_intention ~
    hostility_score +
    norm_of_retaliation +
    dehumanization +
    perceived_injustice +
    material_conflict_index +
    identity_threat_index +
    legitimacy_index +
    cooperative_contact_index +
    condition +
    context_type +
    (1 | participant) +
    (1 | dyad_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

exclusion_model <- lmer(
  support_for_exclusion ~
    hostility_score +
    symbolic_threat +
    realistic_threat +
    status_threat +
    dehumanization +
    stereotype_endorsement +
    legitimacy_index +
    cooperative_contact_index +
    condition +
    context_type +
    (1 | participant) +
    (1 | dyad_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

cooperation_model <- lmer(
  support_for_cooperation ~
    cooperative_contact_index +
    common_goal_salience +
    equal_status +
    institutional_support +
    legitimacy_index +
    cooperative_task_success +
    hostility_score +
    zero_sum_perception +
    condition +
    context_type +
    (1 | participant) +
    (1 | dyad_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

response_time_model <- lmer(
  log_response_time ~
    hostility_score +
    intergroup_anxiety +
    symbolic_threat +
    realistic_threat +
    cooperative_contact_index +
    legitimacy_index +
    condition +
    context_type +
    (1 | participant) +
    (1 | dyad_id) +
    (1 | scenario_id) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    hostility_model = summary(hostility_model),
    aggression_model = summary(aggression_model),
    exclusion_model = summary(exclusion_model),
    cooperation_model = summary(cooperation_model),
    response_time_model = summary(response_time_model),
    condition_hostility = emmeans(hostility_model, ~ condition),
    diagnostics = check_model(hostility_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(hostility_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_hostility_coefficients.csv"))
write_csv(tidy(aggression_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_aggression_coefficients.csv"))
write_csv(tidy(exclusion_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_exclusion_coefficients.csv"))
write_csv(tidy(cooperation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_cooperation_coefficients.csv"))

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    mean_hostility = mean(hostility_score, na.rm = TRUE),
    mean_aggression = mean(aggression_intention, na.rm = TRUE),
    mean_exclusion = mean(support_for_exclusion, na.rm = TRUE),
    mean_cooperation = mean(support_for_cooperation, na.rm = TRUE),
    mean_contact = mean(cooperative_contact_index, na.rm = TRUE),
    mean_legitimacy = mean(legitimacy_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_summary_by_condition.csv"))

p <- ggplot(condition_summary, aes(x = reorder(condition, mean_hostility), y = mean_hostility, group = 1)) +
  geom_line() +
  geom_point() +
  coord_flip() +
  labs(
    title = "Mean intergroup hostility by condition",
    x = "Condition",
    y = "Mean hostility score"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_hostility_by_condition_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
