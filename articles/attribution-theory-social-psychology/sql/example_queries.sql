-- Example analytical queries for attribution theory research.

-- 1. Summary by condition, target, valence, and context.
SELECT
    condition,
    target_type,
    outcome_valence,
    institution_context,
    n_trials,
    n_participants,
    mean_internal,
    mean_external,
    mean_disposition_bias,
    mean_responsibility,
    mean_blame,
    mean_help,
    mean_hostile_attribution
FROM attribution_summary
ORDER BY mean_responsibility DESC;

-- 2. Actor-observer asymmetry.
SELECT
    self_other,
    outcome_valence,
    COUNT(*) AS n,
    AVG(attribution_internal) AS mean_internal,
    AVG(attribution_external) AS mean_external,
    AVG(disposition_bias_index) AS mean_disposition_bias
FROM attribution_trials
GROUP BY self_other, outcome_valence
ORDER BY outcome_valence, self_other;

-- 3. Covariation cues and external attribution.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(consensus) AS mean_consensus,
    AVG(distinctiveness) AS mean_distinctiveness,
    AVG(consistency) AS mean_consistency,
    AVG(covariation_situation_index) AS mean_covariation_situation,
    AVG(attribution_external) AS mean_external
FROM attribution_trials
GROUP BY condition
ORDER BY mean_external DESC;

-- 4. Responsibility and emotion.
SELECT
    outcome_valence,
    target_type,
    COUNT(*) AS n,
    AVG(responsibility_rating) AS mean_responsibility,
    AVG(blame_rating) AS mean_blame,
    AVG(sympathy_rating) AS mean_sympathy,
    AVG(anger_rating) AS mean_anger,
    AVG(punishment_support) AS mean_punishment,
    AVG(help_support) AS mean_help
FROM attribution_trials
GROUP BY outcome_valence, target_type
ORDER BY mean_blame DESC;

-- 5. Hostile attribution under ambiguity and intergroup context.
SELECT
    target_type,
    condition,
    COUNT(*) AS n,
    AVG(ambiguity_level) AS mean_ambiguity,
    AVG(hostile_attribution_score) AS mean_hostile_attribution,
    AVG(attributional_complexity) AS mean_attributional_complexity
FROM attribution_trials
GROUP BY target_type, condition
ORDER BY mean_hostile_attribution DESC;
