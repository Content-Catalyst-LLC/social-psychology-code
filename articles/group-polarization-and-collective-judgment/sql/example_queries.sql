-- Example analytical queries for group polarization and collective judgment research.

-- 1. Summary by condition and platform context.
SELECT
    condition,
    platform_context,
    n_trials,
    n_participants,
    n_groups,
    mean_pre_attitude,
    mean_post_attitude,
    mean_attitude_shift,
    mean_extremity_shift,
    mean_confidence_shift,
    mean_polarization_risk,
    mean_deliberative_safeguards,
    mean_decision_quality,
    mean_collective_accuracy
FROM group_polarization_summary
ORDER BY mean_extremity_shift DESC;

-- 2. High-risk polarization audit.
SELECT
    condition,
    platform_context,
    COUNT(*) AS n,
    AVG(extremity_shift) AS mean_extremity_shift,
    AVG(confidence_shift) AS mean_confidence_shift,
    AVG(polarization_risk_index) AS mean_risk,
    AVG(deliberative_safeguard_index) AS mean_safeguards,
    AVG(decision_quality) AS mean_quality,
    AVG(collective_judgment_accuracy) AS mean_accuracy
FROM high_risk_polarization_cases
GROUP BY condition, platform_context
ORDER BY mean_risk DESC;

-- 3. Deliberative safeguards and judgment quality.
SELECT
    CASE
        WHEN deliberative_safeguard_index < 3 THEN 'weak_safeguards'
        WHEN deliberative_safeguard_index < 7 THEN 'moderate_safeguards'
        ELSE 'strong_safeguards'
    END AS safeguard_band,
    COUNT(*) AS n,
    AVG(extremity_shift) AS mean_extremity_shift,
    AVG(confidence_shift) AS mean_confidence_shift,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(collective_judgment_accuracy) AS mean_accuracy
FROM group_polarization_trials
GROUP BY safeguard_band
ORDER BY mean_accuracy DESC;

-- 4. Algorithmic reinforcement and cross-cutting exposure.
SELECT
    condition,
    platform_context,
    AVG(algorithmic_reinforcement) AS mean_algorithmic_reinforcement,
    AVG(cross_cutting_exposure) AS mean_cross_cutting_exposure,
    AVG(informational_homogeneity) AS mean_homogeneity,
    AVG(extremity_shift) AS mean_extremity_shift,
    AVG(perceived_consensus) AS mean_consensus,
    AVG(collective_judgment_accuracy) AS mean_accuracy
FROM group_polarization_trials
WHERE platform_context IN ('platform_feed', 'online_forum')
GROUP BY condition, platform_context
ORDER BY mean_extremity_shift DESC;

-- 5. Dissent quality and polarization.
SELECT
    dissent_presence,
    CASE
        WHEN dissent_quality < 3 THEN 'weak_dissent'
        WHEN dissent_quality < 7 THEN 'moderate_dissent'
        ELSE 'strong_dissent'
    END AS dissent_band,
    COUNT(*) AS n,
    AVG(argument_diversity) AS mean_argument_diversity,
    AVG(extremity_shift) AS mean_extremity_shift,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(collective_judgment_accuracy) AS mean_accuracy
FROM group_polarization_trials
GROUP BY dissent_presence, dissent_band
ORDER BY mean_accuracy DESC;
