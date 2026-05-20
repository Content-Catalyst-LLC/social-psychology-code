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
input_path <- ifelse(length(args) >= 1, args[[1]], "data/contact_hypothesis_trials.csv")
output_dir <- ifelse(length(args) >= 2, args[[2]], "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

dat <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(
    participant = factor(participant),
    site_id = factor(site_id),
    condition = factor(condition),
    target_group = factor(target_group),
    group_status = factor(group_status),
    prejudice_change = prejudice_post - prejudice_pre,
    allport_quality = rowMeans(across(c(equal_status, common_goals, cooperation, institutional_support, voluntariness)), na.rm = TRUE),
    log_response_time = log(response_time_ms)
  )

condition_summary <- dat %>%
  group_by(condition) %>%
  summarise(
    n = n(),
    participants = n_distinct(participant),
    sites = n_distinct(site_id),
    mean_contact_frequency = mean(contact_frequency, na.rm = TRUE),
    mean_contact_quality = mean(contact_quality, na.rm = TRUE),
    mean_allport_quality = mean(allport_quality, na.rm = TRUE),
    mean_negative_contact = mean(negative_contact, na.rm = TRUE),
    mean_indirect_contact = mean(indirect_contact, na.rm = TRUE),
    mean_anxiety = mean(intergroup_anxiety, na.rm = TRUE),
    mean_empathy = mean(empathy, na.rm = TRUE),
    mean_trust = mean(trust, na.rm = TRUE),
    mean_prejudice_pre = mean(prejudice_pre, na.rm = TRUE),
    mean_prejudice_post = mean(prejudice_post, na.rm = TRUE),
    mean_prejudice_change = mean(prejudice_change, na.rm = TRUE),
    mean_social_distance = mean(social_distance, na.rm = TRUE),
    mean_future_contact = mean(future_contact_willingness, na.rm = TRUE),
    .groups = "drop"
  )

write_csv(condition_summary, file.path(output_dir, "r_summary_by_condition.csv"))

prejudice_model <- lmer(
  prejudice_post ~
    prejudice_pre +
    condition +
    group_status +
    contact_frequency +
    contact_quality +
    allport_quality +
    negative_contact +
    indirect_contact +
    intergroup_anxiety +
    empathy +
    perspective_taking +
    trust +
    perceived_threat +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

change_model <- lmer(
  prejudice_change ~
    condition +
    group_status +
    contact_frequency +
    contact_quality +
    allport_quality +
    negative_contact +
    indirect_contact +
    intergroup_anxiety +
    empathy +
    trust +
    perceived_threat +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

anxiety_model <- lmer(
  intergroup_anxiety ~
    condition +
    contact_frequency +
    contact_quality +
    allport_quality +
    negative_contact +
    indirect_contact +
    group_status +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

empathy_model <- lmer(
  empathy ~
    condition +
    contact_frequency +
    contact_quality +
    allport_quality +
    negative_contact +
    indirect_contact +
    group_status +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

social_distance_model <- lmer(
  social_distance ~
    prejudice_post +
    contact_quality +
    negative_contact +
    intergroup_anxiety +
    empathy +
    trust +
    perceived_threat +
    group_status +
    (1 | participant) +
    (1 | site_id),
  data = dat,
  REML = FALSE
)

rt_model <- lmer(
  log_response_time ~
    condition +
    contact_quality +
    negative_contact +
    intergroup_anxiety +
    empathy +
    trust +
    prejudice_post +
    perceived_threat +
    (1 | participant) +
    (1 | site_id),
  data = dat %>% filter(response_time_ms >= 150),
  REML = FALSE
)

capture.output(
  list(
    prejudice_model = summary(prejudice_model),
    prejudice_change_model = summary(change_model),
    anxiety_model = summary(anxiety_model),
    empathy_model = summary(empathy_model),
    social_distance_model = summary(social_distance_model),
    response_time_model = summary(rt_model),
    prejudice_by_condition = emmeans(prejudice_model, ~ condition),
    change_by_condition = emmeans(change_model, ~ condition),
    diagnostics = check_model(prejudice_model)
  ),
  file = file.path(output_dir, "r_model_summaries.txt")
)

write_csv(tidy(prejudice_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_prejudice_model_coefficients.csv"))
write_csv(tidy(change_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_prejudice_change_coefficients.csv"))
write_csv(tidy(anxiety_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_anxiety_coefficients.csv"))
write_csv(tidy(empathy_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_empathy_coefficients.csv"))
write_csv(tidy(social_distance_model, effects = "fixed", conf.int = TRUE), file.path(output_dir, "r_social_distance_coefficients.csv"))

p <- ggplot(dat, aes(x = contact_quality, y = prejudice_post, color = condition)) +
  geom_point(alpha = 0.30) +
  geom_smooth(method = "lm", se = FALSE) +
  labs(
    title = "Contact quality and post-contact prejudice",
    x = "Contact quality",
    y = "Post-contact prejudice score"
  ) +
  theme_minimal(base_size = 12)

ggsave(file.path(output_dir, "r_contact_quality_prejudice_plot.png"), p, width = 9, height = 6, dpi = 300)

message("R analysis complete. Outputs written to: ", output_dir)
