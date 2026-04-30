# Synthetic social psychology analysis.
# Run after the Python script creates data/processed/synthetic_social_trials.csv.

data_path <- file.path("data", "processed", "synthetic_social_trials.csv")

if (!file.exists(data_path)) {
  stop("Run: python3 python/social_psychology_simulation.py")
}

dat <- read.csv(data_path)

summary_table <- aggregate(
  cbind(attribution_internal, attribution_external, trust_rating, warmth_rating, competence_rating) ~
    target_group + condition + schema_consistent,
  data = dat,
  FUN = mean
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_table, file.path("outputs", "social_judgment_summary.csv"), row.names = FALSE)

print(summary_table)
