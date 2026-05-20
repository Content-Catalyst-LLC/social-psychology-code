-- Example analytical queries for diffusion-of-responsibility research.

-- 1. Summary by condition and scenario domain.
SELECT
    condition,
    scenario_domain,
    n_trials,
    mean_bystanders,
    intervention_rate,
    reporting_rate,
    mean_delay_seconds,
    mean_responsibility,
    mean_role_clarity,
    mean_ambiguity,
    mean_pluralistic_gap
FROM diffusion_summary
ORDER BY condition, scenario_domain;

-- 2. Bystander bands and intervention rate.
SELECT
    CASE
        WHEN bystander_count = 0 THEN 'alone'
        WHEN bystander_count <= 2 THEN 'small'
        WHEN bystander_count <= 6 THEN 'medium'
        ELSE 'large'
    END AS bystander_band,
    COUNT(*) AS n,
    AVG(intervention_decision) AS intervention_rate,
    AVG(reporting_decision) AS reporting_rate,
    AVG(perceived_responsibility) AS mean_responsibility,
    AVG(intervention_delay_seconds) AS mean_delay_seconds
FROM diffusion_trials
GROUP BY bystander_band
ORDER BY bystander_band;

-- 3. Role clarity and diffusion.
SELECT
    CASE
        WHEN role_clarity < 3 THEN 'low_clarity'
        WHEN role_clarity < 7 THEN 'moderate_clarity'
        ELSE 'high_clarity'
    END AS role_clarity_band,
    COUNT(*) AS n,
    AVG(intervention_decision) AS intervention_rate,
    AVG(perceived_responsibility) AS mean_responsibility,
    AVG(organizational_fragmentation) AS mean_fragmentation,
    AVG(ambiguity_level) AS mean_ambiguity
FROM diffusion_trials
GROUP BY role_clarity_band;

-- 4. Pluralistic ignorance gap and nonintervention.
SELECT
    CASE
        WHEN pluralistic_ignorance_gap < 1 THEN 'low_gap'
        WHEN pluralistic_ignorance_gap < 3 THEN 'moderate_gap'
        ELSE 'high_gap'
    END AS pluralistic_gap_band,
    COUNT(*) AS n,
    AVG(intervention_decision) AS intervention_rate,
    AVG(private_concern) AS mean_private_concern,
    AVG(perceived_group_concern) AS mean_perceived_group_concern,
    AVG(evaluation_apprehension) AS mean_evaluation
FROM diffusion_trials
GROUP BY pluralistic_gap_band;
