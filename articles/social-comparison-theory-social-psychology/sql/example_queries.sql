-- Example analytical queries for social comparison research.

-- 1. Summary by condition and comparison type.
SELECT
    condition,
    comparison_type,
    n_trials,
    mean_gap,
    mean_attainability,
    mean_self_eval_change,
    mean_motivation,
    mean_envy,
    mean_inspiration,
    mean_discouragement,
    mean_relative_deprivation
FROM comparison_type_summary
ORDER BY condition, comparison_type;

-- 2. Upward comparison by attainability band.
SELECT
    CASE
        WHEN attainability < 3 THEN 'low_attainability'
        WHEN attainability < 7 THEN 'moderate_attainability'
        ELSE 'high_attainability'
    END AS attainability_band,
    COUNT(*) AS n,
    AVG(self_eval_change) AS mean_self_eval_change,
    AVG(motivation_score) AS mean_motivation,
    AVG(envy) AS mean_envy,
    AVG(inspiration) AS mean_inspiration,
    AVG(discouragement) AS mean_discouragement
FROM social_comparison_trials
WHERE comparison_type = 'upward'
GROUP BY attainability_band
ORDER BY attainability_band;

-- 3. Digital exposure and comparison effects.
SELECT
    CASE
        WHEN digital_exposure < 3 THEN 'low_digital_exposure'
        WHEN digital_exposure < 7 THEN 'moderate_digital_exposure'
        ELSE 'high_digital_exposure'
    END AS digital_exposure_band,
    COUNT(*) AS n,
    AVG(comparison_gap) AS mean_gap,
    AVG(self_eval_change) AS mean_self_eval_change,
    AVG(relative_deprivation) AS mean_relative_deprivation,
    AVG(envy) AS mean_envy,
    AVG(discouragement) AS mean_discouragement
FROM social_comparison_trials
GROUP BY digital_exposure_band;

-- 4. Identity-relevant domains.
SELECT
    comparison_domain,
    comparison_type,
    COUNT(*) AS n,
    AVG(identity_relevance) AS mean_identity_relevance,
    AVG(self_eval_change) AS mean_self_eval_change,
    AVG(motivation_score) AS mean_motivation,
    AVG(relative_deprivation) AS mean_relative_deprivation
FROM social_comparison_trials
GROUP BY comparison_domain, comparison_type;
