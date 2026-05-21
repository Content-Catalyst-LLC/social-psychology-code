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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/deindividuation_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    session_id = factor(session_id),
    group_id = factor(group_id),
    site_id = factor(site_id),
    condition = factor(condition),
    context_type = factor(context_type),
    log_group_size = log1p(group_size),
    identity_shift_index = group_identity_salience - personal_identity_salience,
    deindividuation_index = (
      anonymity +
      crowd_immersion +
      responsibility_diffusion +
      arousal_index -
      self_awareness -
      accountability
    ) / 4,
    side_norm_activation = (
      anonymity *
      group_identity_salience *
      norm_clarity
    ) / 100,
    antisocial_norm = as.integer(group_norm_valence < 0),
    prosocial_norm = as.integer(group_norm_valence > 0),
    log_response_time = log(response_time_ms)
  )

summary_table <- dat %>%
  group_by(condition, context_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_behavior = mean(behavior_score, na.rm = TRUE),
    mean_prosocial = mean(prosocial_behavior, na.rm = TRUE),
    mean_antisocial = mean(antisocial_behavior, na.rm = TRUE),
    mean_anonymity = mean(anonymity, na.rm = TRUE),
    mean_self_awareness = mean(self_awareness, na.rm = TRUE),
    mean_accountability = mean(accountability, na.rm = TRUE),
    mean_group_identity = mean(group_identity_salience, na.rm = TRUE),
    mean_norm_congruence = mean(norm_congruence, na.rm = TRUE),
    mean_deindividuation = mean(deindividuation_index, na.rm = TRUE),
    mean_response_time = mean(response_time_ms, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(summary_table, file.path(output_dir, "r_summary_by_condition_context.csv"))

norm_model <- lmer(
  norm_congruence ~
    anonymity * group_identity_salience * group_norm_valence +
    self_awareness +
    accountability +
    norm_clarity +
    crowd_immersion +
    perceived_surveillance +
    moderation_visibility +
    condition +
    context_type +
    (1 + anonymity | participant) +
    (1 | group_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

prosocial_model <- lmer(
  prosocial_behavior ~
    anonymity * group_identity_salience * group_norm_valence +
    norm_congruence +
    self_awareness +
    accountability +
    moral_disengagement +
    moderation_visibility +
    condition +
    context_type +
    (1 | participant) +
    (1 | group_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

antisocial_model <- lmer(
  antisocial_behavior ~
    anonymity * group_identity_salience * group_norm_valence +
    norm_congruence +
    responsibility_diffusion +
    moral_disengagement +
    accountability +
    moderation_visibility +
    self_awareness +
    condition +
    context_type +
    (1 | participant) +
    (1 | group_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

deindividuation_model <- lmer(
  deindividuation_index ~
    anonymity +
    identifiability +
    log_group_size +
    crowd_immersion +
    group_identity_salience +
    personal_identity_salience +
    accountability +
    moderation_visibility +
    condition +
    context_type +
    (1 | participant) +
    (1 | group_id) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    deindividuation_index +
    norm_clarity +
    arousal_index +
    self_awareness +
    accountability +
    condition +
    context_type +
    (1 | participant) +
    (1 | group_id) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    norm_congruence_model = summary(norm_model),
    prosocial_model = summary(prosocial_model),
    antisocial_model = summary(antisocial_model),
    deindividuation_model = summary(deindividuation_model),
    response_time_model = summary(rt_model),
    anonymity_by_group_identity = emmeans(norm_model, ~ anonymity | group_identity_salience),
    diagnostics = check_model(norm_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(norm_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_norm_congruence_coefficients.csv"))
write_csv(tidy(prosocial_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_prosocial_coefficients.csv"))
write_csv(tidy(antisocial_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_antisocial_coefficients.csv"))
write_csv(tidy(deindividuation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_deindividuation_coefficients.csv"))

norm_summary <- dat %>%
  mutate(
    norm_band = cut(
      group_norm_valence,
      breaks = c(-5.1, -1.0, 1.0, 5.1),
      labels = c("antisocial_norm", "neutral_norm", "prosocial_norm")
    )
  ) %>%
  group_by(condition, norm_band) %>%
  summarise(
    n = n(),
    mean_norm_congruence = mean(norm_congruence, na.rm = TRUE),
    mean_prosocial = mean(prosocial_behavior, na.rm = TRUE),
    mean_antisocial = mean(antisocial_behavior, na.rm = TRUE),
    mean_deindividuation = mean(deindividuation_index, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(norm_summary, file.path(output_dir, "r_summary_by_condition_norm_valence.csv"))

p <- ggplot(norm_summary, aes(x = norm_band, y = mean_norm_congruence, color = condition, group = condition)) +
  geom_line() +
  geom_point() +
  labs(
    title = "Norm congruence under anonymity and salient norms",
    x = "Group norm valence",
    y = "Mean norm congruence"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_norm_congruence_by_valence_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
