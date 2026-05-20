-- Example analytical queries for in-group bias research.

-- 1. Trust, fairness, and allocation by target relation.
SELECT
    condition,
    target_group_relation,
    n_trials,
    mean_trust,
    mean_fairness,
    mean_resource,
    mean_blame,
    mean_punishment,
    cooperation_rate
FROM target_relation_summary
ORDER BY condition, target_group_relation;

-- 2. Condition-level bias differentials.
SELECT
    ing.condition,
    ing.mean_trust - out.mean_trust AS trust_bias,
    ing.mean_fairness - out.mean_fairness AS fairness_bias,
    ing.mean_resource - out.mean_resource AS resource_bias,
    out.mean_blame - ing.mean_blame AS blame_asymmetry,
    out.mean_punishment - ing.mean_punishment AS punishment_asymmetry
FROM target_relation_summary ing
JOIN target_relation_summary out
    ON ing.condition = out.condition
WHERE ing.target_group_relation = 'ingroup'
  AND out.target_group_relation = 'outgroup'
ORDER BY trust_bias DESC;

-- 3. Institutional-context bias patterns.
SELECT
    institutional_context,
    target_group_relation,
    COUNT(*) AS n,
    AVG(trust_rating) AS mean_trust,
    AVG(resource_allocation) AS mean_resource,
    AVG(moral_blame) AS mean_blame,
    AVG(punishment_severity) AS mean_punishment
FROM ingroup_bias_trials
GROUP BY institutional_context, target_group_relation
ORDER BY institutional_context, target_group_relation;

-- 4. Threat and identity salience bands.
SELECT
    CASE
        WHEN identity_salience < 3 THEN 'low_identity_salience'
        WHEN identity_salience < 7 THEN 'medium_identity_salience'
        ELSE 'high_identity_salience'
    END AS identity_salience_band,
    CASE
        WHEN perceived_threat < 3 THEN 'low_threat'
        WHEN perceived_threat < 7 THEN 'medium_threat'
        ELSE 'high_threat'
    END AS threat_band,
    target_group_relation,
    COUNT(*) AS n,
    AVG(trust_rating) AS mean_trust,
    AVG(resource_allocation) AS mean_resource,
    AVG(moral_blame) AS mean_blame
FROM ingroup_bias_trials
GROUP BY identity_salience_band, threat_band, target_group_relation;
