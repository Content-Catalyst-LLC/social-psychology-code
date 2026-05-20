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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/ingroup_bias_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    target_group_relation = factor(target_group_relation),
    institutional_context = factor(institutional_context),
    ingroup_target = as.integer(ingroup_target),
    cooperation_choice = as.integer(cooperation_choice),
    log_response_time = log(response_time_ms)
  )

relation_summary <- dat %>%
  group_by(condition, target_group_relation) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_trust = mean(trust_rating, na.rm = TRUE),
    mean_fairness = mean(fairness_rating, na.rm = TRUE),
    mean_competence = mean(competence_rating, na.rm = TRUE),
    mean_warmth = mean(warmth_rating, na.rm = TRUE),
    mean_empathy = mean(empathy_rating, na.rm = TRUE),
    mean_blame = mean(moral_blame, na.rm = TRUE),
    mean_forgiveness = mean(moral_forgiveness, na.rm = TRUE),
    mean_punishment = mean(punishment_severity, na.rm = TRUE),
    mean_reward = mean(reward_allocation, na.rm = TRUE),
    mean_resource = mean(resource_allocation, na.rm = TRUE),
    cooperation_rate = mean(cooperation_choice, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(relation_summary, file.path(output_dir, "r_summary_by_condition_target_relation.csv"))

trust_model <- lmer(
  trust_rating ~
    ingroup_target * identity_salience +
    group_identification +
    perceived_threat +
    norm_strength +
    status_asymmetry +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

fairness_model <- lmer(
  fairness_rating ~
    ingroup_target * identity_salience +
    group_identification +
    perceived_threat +
    norm_strength +
    status_asymmetry +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

allocation_model <- lmer(
  resource_allocation ~
    ingroup_target * identity_salience +
    group_identification +
    perceived_threat +
    norm_strength +
    status_asymmetry +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

moral_blame_model <- lmer(
  moral_blame ~
    ingroup_target * identity_salience +
    group_identification +
    perceived_threat +
    norm_strength +
    status_asymmetry +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

punishment_model <- lmer(
  punishment_severity ~
    ingroup_target * identity_salience +
    group_identification +
    perceived_threat +
    norm_strength +
    status_asymmetry +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

cooperation_model <- glmer(
  cooperation_choice ~
    ingroup_target * identity_salience +
    trust_rating +
    perceived_threat +
    norm_strength +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  family = binomial(),
  control = glmerControl(optimizer = "bobyqa")
)

rt_model <- lmer(
  log_response_time ~
    ingroup_target * identity_salience +
    perceived_threat +
    norm_strength +
    condition +
    institutional_context +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    trust_model = summary(trust_model),
    fairness_model = summary(fairness_model),
    allocation_model = summary(allocation_model),
    moral_blame_model = summary(moral_blame_model),
    punishment_model = summary(punishment_model),
    cooperation_model = summary(cooperation_model),
    response_time_model = summary(rt_model),
    trust_by_target = emmeans(trust_model, ~ ingroup_target),
    allocation_by_target = emmeans(allocation_model, ~ ingroup_target),
    moral_blame_by_target = emmeans(moral_blame_model, ~ ingroup_target),
    diagnostics = check_model(trust_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(trust_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_trust_coefficients.csv"))
write_csv(tidy(fairness_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_fairness_coefficients.csv"))
write_csv(tidy(allocation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_allocation_coefficients.csv"))
write_csv(tidy(moral_blame_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_moral_blame_coefficients.csv"))
write_csv(tidy(cooperation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_cooperation_coefficients.csv"))

p <- ggplot(dat, aes(x = identity_salience, y = trust_rating, color = target_group_relation)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Identity salience and trust by target group relation",
    x = "Identity salience",
    y = "Trust rating"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_identity_salience_trust_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
