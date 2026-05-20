-- Example analytical queries for social dilemma research.

-- 1. Summary by condition, dilemma type, and round.
SELECT
    condition,
    dilemma_type,
    round,
    n_trials,
    mean_contribution,
    mean_extraction,
    mean_free_riding,
    mean_trust,
    mean_norm_salience,
    mean_enforcement,
    mean_legitimacy,
    mean_group_welfare,
    mean_resource_stock
FROM social_dilemma_summary
ORDER BY condition, dilemma_type, round;

-- 2. Institutional conditions and cooperation.
SELECT
    condition,
    dilemma_type,
    COUNT(*) AS n,
    AVG(contribution) AS mean_contribution,
    AVG(extraction) AS mean_extraction,
    AVG(institutional_effectiveness) AS mean_institutional_effectiveness,
    AVG(institutional_legitimacy) AS mean_legitimacy,
    AVG(group_welfare) AS mean_group_welfare
FROM social_dilemma_trials
GROUP BY condition, dilemma_type
ORDER BY mean_group_welfare DESC;

-- 3. Public-goods game MPCR check.
SELECT
    group_id,
    condition,
    COUNT(DISTINCT participant) AS group_size,
    AVG(mpcr) AS mpcr,
    CASE
        WHEN AVG(mpcr) > 0 AND AVG(mpcr) < 1 AND COUNT(DISTINCT participant) * AVG(mpcr) > 1
        THEN 'public_goods_dilemma_condition_met'
        ELSE 'check_parameters'
    END AS mpcr_validation
FROM social_dilemma_trials
WHERE dilemma_type IN ('public_goods', 'threshold_public_good', 'nested_public_good')
GROUP BY group_id, condition;

-- 4. Commons depletion risk.
SELECT
    condition,
    round,
    AVG(resource_stock) AS mean_resource_stock,
    AVG(extraction) AS mean_extraction,
    AVG(monitoring_strength) AS mean_monitoring,
    AVG(institutional_legitimacy) AS mean_legitimacy
FROM social_dilemma_trials
WHERE dilemma_type = 'commons'
GROUP BY condition, round
ORDER BY condition, round;
