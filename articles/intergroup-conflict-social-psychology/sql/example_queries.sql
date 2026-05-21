-- Example analytical queries for intergroup conflict research.

-- 1. Summary by condition and context.
SELECT
    condition,
    context_type,
    n_trials,
    n_participants,
    n_groups,
    n_dyads,
    mean_hostility,
    mean_aggression,
    mean_avoidance,
    mean_exclusion,
    mean_cooperation,
    mean_material_conflict,
    mean_identity_threat,
    mean_contact,
    mean_legitimacy
FROM intergroup_conflict_summary
ORDER BY mean_hostility DESC;

-- 2. Contact and cooperation effects.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(contact_quality) AS mean_contact_quality,
    AVG(equal_status) AS mean_equal_status,
    AVG(common_goal_salience) AS mean_common_goal,
    AVG(institutional_support) AS mean_institutional_support,
    AVG(hostility_score) AS mean_hostility,
    AVG(support_for_cooperation) AS mean_cooperation
FROM intergroup_conflict_trials
WHERE condition IN ('contact_intervention', 'superordinate_goal', 'baseline')
GROUP BY condition
ORDER BY mean_cooperation DESC;

-- 3. High-risk escalation audit.
SELECT
    condition,
    context_type,
    COUNT(*) AS n,
    AVG(material_conflict_index) AS mean_material_conflict,
    AVG(identity_threat_index) AS mean_identity_threat,
    AVG(symbolic_threat) AS mean_symbolic_threat,
    AVG(realistic_threat) AS mean_realistic_threat,
    AVG(dehumanization) AS mean_dehumanization,
    AVG(norm_of_retaliation) AS mean_retaliation_norm,
    AVG(group_polarization) AS mean_polarization,
    AVG(hostility_score) AS mean_hostility,
    AVG(aggression_intention) AS mean_aggression,
    AVG(support_for_exclusion) AS mean_exclusion
FROM high_risk_escalation_cases
GROUP BY condition, context_type
ORDER BY mean_hostility DESC;

-- 4. Legitimacy and conflict outcomes.
SELECT
    CASE
        WHEN legitimacy_index < 3 THEN 'low_legitimacy'
        WHEN legitimacy_index < 7 THEN 'moderate_legitimacy'
        ELSE 'high_legitimacy'
    END AS legitimacy_band,
    COUNT(*) AS n,
    AVG(hostility_score) AS mean_hostility,
    AVG(aggression_intention) AS mean_aggression,
    AVG(support_for_exclusion) AS mean_exclusion,
    AVG(support_for_cooperation) AS mean_cooperation
FROM intergroup_conflict_trials
GROUP BY legitimacy_band
ORDER BY mean_hostility DESC;

-- 5. Material versus symbolic threat.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(resource_competition) AS mean_resource_competition,
    AVG(realistic_threat) AS mean_realistic_threat,
    AVG(symbolic_threat) AS mean_symbolic_threat,
    AVG(status_threat) AS mean_status_threat,
    AVG(hostility_score) AS mean_hostility,
    AVG(support_for_exclusion) AS mean_exclusion
FROM intergroup_conflict_trials
GROUP BY condition
ORDER BY mean_hostility DESC;
