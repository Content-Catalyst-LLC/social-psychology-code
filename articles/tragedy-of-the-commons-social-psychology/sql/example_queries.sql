-- Example analytical queries for tragedy-of-the-commons research.

-- 1. Summary by governance condition, property regime, and round.
SELECT
    condition,
    property_regime,
    round,
    n_trials,
    mean_extraction,
    mean_resource_stock,
    mean_regeneration,
    mean_depletion_risk,
    mean_trust,
    mean_legitimacy,
    mean_monitoring,
    mean_institutional_effectiveness,
    mean_group_welfare
FROM commons_governance_summary
ORDER BY condition, property_regime, round;

-- 2. Compare open access with governed commons.
SELECT
    property_regime,
    COUNT(*) AS n,
    AVG(extraction) AS mean_extraction,
    AVG(resource_stock) AS mean_resource_stock,
    AVG(depletion_risk) AS mean_depletion_risk,
    AVG(legitimacy_score) AS mean_legitimacy,
    AVG(boundary_clarity) AS mean_boundary_clarity,
    AVG(rule_participation) AS mean_rule_participation,
    AVG(institutional_effectiveness) AS mean_institutional_effectiveness
FROM commons_trials
GROUP BY property_regime
ORDER BY mean_depletion_risk DESC;

-- 3. Sustainability threshold check.
SELECT
    group_id,
    round,
    SUM(extraction) AS total_extraction,
    AVG(sustainable_threshold) AS sustainable_threshold,
    CASE
        WHEN SUM(extraction) > AVG(sustainable_threshold)
        THEN 'over_sustainable_threshold'
        ELSE 'within_sustainable_threshold'
    END AS sustainability_status
FROM commons_trials
GROUP BY group_id, round
ORDER BY group_id, round;

-- 4. High-depletion cases for audit.
SELECT
    condition,
    property_regime,
    round,
    COUNT(*) AS n,
    AVG(extraction) AS mean_extraction,
    AVG(depletion_risk) AS mean_depletion_risk,
    AVG(trust_score) AS mean_trust,
    AVG(legitimacy_score) AS mean_legitimacy,
    AVG(asymmetry_index) AS mean_asymmetry
FROM high_depletion_risk_cases
GROUP BY condition, property_regime, round
ORDER BY mean_depletion_risk DESC;
