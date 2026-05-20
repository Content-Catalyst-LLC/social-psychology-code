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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/social_comparison_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    comparison_type = factor(comparison_type),
    comparison_domain = factor(comparison_domain),
    reference_group = factor(reference_group),
    self_eval_change = self_eval_post - self_eval_pre,
    log_response_time = log(response_time_ms)
  )

comparison_summary <- dat %>%
  group_by(condition, comparison_type) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    mean_gap = mean(comparison_gap, na.rm = TRUE),
    mean_attainability = mean(attainability, na.rm = TRUE),
    mean_similarity = mean(similarity, na.rm = TRUE),
    mean_identity_relevance = mean(identity_relevance, na.rm = TRUE),
    mean_self_eval_change = mean(self_eval_change, na.rm = TRUE),
    mean_motivation = mean(motivation_score, na.rm = TRUE),
    mean_envy = mean(envy, na.rm = TRUE),
    mean_inspiration = mean(inspiration, na.rm = TRUE),
    mean_discouragement = mean(discouragement, na.rm = TRUE),
    mean_reassurance = mean(reassurance, na.rm = TRUE),
    mean_self_esteem = mean(self_esteem, na.rm = TRUE),
    mean_relative_deprivation = mean(relative_deprivation, na.rm = TRUE),
    mean_norm_perception = mean(norm_perception, na.rm = TRUE),
    mean_digital_exposure = mean(digital_exposure, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(comparison_summary, file.path(output_dir, "r_summary_by_condition_comparison_type.csv"))

eval_model <- lmer(
  self_eval_change ~
    comparison_type * attainability +
    comparison_gap +
    similarity +
    identity_relevance +
    social_comparison_orientation +
    condition +
    comparison_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

motivation_model <- lmer(
  motivation_score ~
    comparison_type * attainability +
    comparison_gap +
    similarity +
    identity_relevance +
    inspiration +
    discouragement +
    condition +
    comparison_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

envy_model <- lmer(
  envy ~
    comparison_gap +
    attainability +
    similarity +
    identity_relevance +
    social_comparison_orientation +
    digital_exposure +
    condition +
    comparison_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

inspiration_model <- lmer(
  inspiration ~
    comparison_type * attainability +
    comparison_gap +
    similarity +
    identity_relevance +
    condition +
    comparison_domain +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

relative_deprivation_model <- lmer(
  relative_deprivation ~
    comparison_gap +
    attainability +
    identity_relevance +
    perceived_fairness +
    condition +
    reference_group +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

self_esteem_model <- lmer(
  self_esteem ~
    self_eval_post +
    envy +
    inspiration +
    discouragement +
    reassurance +
    relative_deprivation +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    comparison_type * identity_relevance +
    comparison_gap +
    attainability +
    relative_deprivation +
    social_comparison_orientation +
    condition +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    self_evaluation_change_model = summary(eval_model),
    motivation_model = summary(motivation_model),
    envy_model = summary(envy_model),
    inspiration_model = summary(inspiration_model),
    relative_deprivation_model = summary(relative_deprivation_model),
    self_esteem_model = summary(self_esteem_model),
    response_time_model = summary(rt_model),
    self_evaluation_by_comparison_type = emmeans(eval_model, ~ comparison_type),
    motivation_by_comparison_type = emmeans(motivation_model, ~ comparison_type),
    diagnostics = check_model(eval_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(eval_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_self_evaluation_coefficients.csv"))
write_csv(tidy(motivation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_motivation_coefficients.csv"))
write_csv(tidy(envy_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_envy_coefficients.csv"))
write_csv(tidy(inspiration_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_inspiration_coefficients.csv"))
write_csv(tidy(relative_deprivation_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_relative_deprivation_coefficients.csv"))

p <- ggplot(dat, aes(x = attainability, y = self_eval_change, color = comparison_type)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Attainability and social comparison effects",
    x = "Attainability",
    y = "Self-evaluation change"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_attainability_self_evaluation_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
