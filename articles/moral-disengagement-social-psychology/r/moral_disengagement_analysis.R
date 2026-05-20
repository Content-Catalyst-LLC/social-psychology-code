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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/moral_disengagement_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

mechanisms <- c(
  "moral_justification", "euphemistic_labeling", "advantageous_comparison",
  "displaced_responsibility", "diffused_responsibility", "consequence_distortion",
  "dehumanization", "blame_attribution"
)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    scenario_domain = factor(scenario_domain),
    harmful_decision = as.integer(harmful_decision),
    md_index = rowMeans(across(all_of(mechanisms)), na.rm = TRUE),
    agency_reduction_index = (displaced_responsibility + diffused_responsibility) / 2,
    harm_obscuration_index = (consequence_distortion + victim_distance - harm_visibility) / 3,
    target_denigration_index = (dehumanization + blame_attribution) / 2,
    self_sanction_index = guilt + empathy + responsibility_clarity,
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, scenario_domain) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_md_index = mean(md_index, na.rm = TRUE),
    harmful_rate = mean(harmful_decision, na.rm = TRUE),
    mean_policy_endorsement = mean(policy_endorsement, na.rm = TRUE),
    mean_unethical_intention = mean(unethical_intention, na.rm = TRUE),
    mean_empathy = mean(empathy, na.rm = TRUE),
    mean_guilt = mean(guilt, na.rm = TRUE),
    mean_harm_visibility = mean(harm_visibility, na.rm = TRUE),
    mean_responsibility_clarity = mean(responsibility_clarity, na.rm = TRUE),
    mean_institutional_pressure = mean(institutional_pressure, na.rm = TRUE),
    mean_authority_pressure = mean(authority_pressure, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_domain.csv"))

harm_model <- glmer(
  harmful_decision ~
    md_index +
    empathy +
    guilt +
    harm_visibility +
    responsibility_clarity +
    institutional_pressure +
    authority_pressure +
    group_norm_strength +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

policy_model <- lmer(
  policy_endorsement ~
    md_index +
    empathy +
    guilt +
    harm_visibility +
    responsibility_clarity +
    institutional_pressure +
    authority_pressure +
    group_norm_strength +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

intention_model <- lmer(
  unethical_intention ~
    md_index +
    empathy +
    guilt +
    perceived_agency +
    responsibility_clarity +
    institutional_pressure +
    authority_pressure +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

empathy_model <- lmer(
  empathy ~
    dehumanization +
    blame_attribution +
    harm_visibility +
    victim_distance +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

guilt_model <- lmer(
  guilt ~
    md_index +
    empathy +
    harm_visibility +
    perceived_agency +
    responsibility_clarity +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

agency_model <- lmer(
  perceived_agency ~
    displaced_responsibility +
    diffused_responsibility +
    authority_pressure +
    responsibility_clarity +
    institutional_pressure +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    md_index +
    guilt +
    responsibility_clarity +
    harmful_decision +
    condition +
    scenario_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

mechanism_long <- dat %>%
  select(participant, condition, scenario_domain, all_of(mechanisms), harmful_decision, policy_endorsement) %>%
  pivot_longer(
    cols = all_of(mechanisms),
    names_to = "mechanism",
    values_to = "score"
  )

mechanism_summary <- mechanism_long %>%
  group_by(condition, mechanism) %>%
  summarise(
    n = n(),
    mean_score = mean(score, na.rm = TRUE),
    harmful_rate = mean(harmful_decision, na.rm = TRUE),
    mean_policy_endorsement = mean(policy_endorsement, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(mechanism_summary, file.path(output_dir, "r_mechanism_summary.csv"))

capture.output(
  list(
    harmful_decision_model = summary(harm_model),
    policy_model = summary(policy_model),
    intention_model = summary(intention_model),
    empathy_model = summary(empathy_model),
    guilt_model = summary(guilt_model),
    agency_model = summary(agency_model),
    response_time_model = summary(rt_model),
    harmful_decision_by_condition = emmeans(harm_model, ~ condition, type = "response"),
    diagnostics = check_model(policy_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(harm_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_harmful_decision_coefficients.csv"))
write_csv(tidy(policy_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_policy_endorsement_coefficients.csv"))
write_csv(tidy(intention_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_unethical_intention_coefficients.csv"))
write_csv(tidy(empathy_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_empathy_coefficients.csv"))
write_csv(tidy(guilt_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_guilt_coefficients.csv"))
write_csv(tidy(agency_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_agency_coefficients.csv"))

p <- ggplot(dat, aes(x = md_index, y = policy_endorsement, color = condition)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Moral disengagement and harmful policy endorsement",
    x = "Moral disengagement index",
    y = "Policy endorsement"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_md_policy_endorsement_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
