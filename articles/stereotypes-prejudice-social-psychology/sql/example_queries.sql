-- Example analytical queries for stereotypes, prejudice, and discrimination research.

-- 1. Summary by condition, institutional context, and target group.
SELECT
    condition,
    institution_context,
    target_group,
    n_trials,
    n_participants,
    mean_stereotype_strength,
    mean_warmth,
    mean_competence,
    mean_prejudice,
    mean_discrimination,
    mean_behavioral_outcome,
    mean_performance,
    mean_contact_support,
    mean_threat_competition,
    mean_decision_structure
FROM stereotypes_prejudice_summary
ORDER BY mean_prejudice DESC;

-- 2. Stereotype content: status and competence, competition and warmth.
SELECT
    target_group,
    AVG(perceived_status) AS mean_status,
    AVG(competence_rating) AS mean_competence,
    AVG(perceived_competition) AS mean_competition,
    AVG(warmth_rating) AS mean_warmth
FROM stereotypes_prejudice_trials
GROUP BY target_group;

-- 3. Contact quality and prejudice.
SELECT
    CASE
        WHEN contact_support_index < 3 THEN 'low_contact_support'
        WHEN contact_support_index < 7 THEN 'moderate_contact_support'
        ELSE 'high_contact_support'
    END AS contact_band,
    COUNT(*) AS n,
    AVG(prejudice_rating) AS mean_prejudice,
    AVG(discrimination_tendency) AS mean_discrimination,
    AVG(social_distance) AS mean_social_distance
FROM stereotypes_prejudice_trials
GROUP BY contact_band
ORDER BY mean_prejudice DESC;

-- 4. Stereotype threat and performance.
SELECT
    CASE
        WHEN stereotype_threat_salience < 3 THEN 'low_threat_salience'
        WHEN stereotype_threat_salience < 7 THEN 'moderate_threat_salience'
        ELSE 'high_threat_salience'
    END AS threat_band,
    COUNT(*) AS n,
    AVG(identity_safety) AS mean_identity_safety,
    AVG(performance_score) AS mean_performance
FROM stereotypes_prejudice_trials
GROUP BY threat_band
ORDER BY mean_performance ASC;

-- 5. High disparity risk.
SELECT
    condition,
    institution_context,
    target_group,
    COUNT(*) AS n,
    AVG(stereotype_strength) AS mean_stereotype_strength,
    AVG(prejudice_rating) AS mean_prejudice,
    AVG(perceived_threat) AS mean_threat,
    AVG(discrimination_tendency) AS mean_discrimination,
    AVG(decision_structure_index) AS mean_decision_structure
FROM high_disparity_risk_cases
GROUP BY condition, institution_context, target_group
ORDER BY n DESC;
