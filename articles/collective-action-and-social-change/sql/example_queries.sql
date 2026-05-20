-- Example analytical queries for collective action research.

-- 1. Participation by experimental condition.
SELECT
    condition,
    n_trials,
    n_participants,
    participation_rate,
    mean_intention,
    mean_identity,
    mean_injustice,
    mean_efficacy,
    mean_cost,
    mean_repression_risk
FROM condition_summary
ORDER BY participation_rate DESC;

-- 2. Digital/offline participation gap.
SELECT
    condition,
    AVG(digital_engagement) AS mean_digital,
    AVG(offline_engagement) AS mean_offline,
    AVG(digital_engagement - offline_engagement) AS mean_digital_offline_gap
FROM collective_action_trials
GROUP BY condition
ORDER BY mean_digital_offline_gap DESC;

-- 3. High-identity, high-cost cases.
SELECT *
FROM high_cost_high_identity_cases
ORDER BY participation_intention DESC;

-- 4. Movement outcome by institutional response.
SELECT
    institutional_response,
    COUNT(*) AS n,
    AVG(action_participation) AS participation_rate,
    AVG(collective_efficacy) AS mean_efficacy,
    AVG(perceived_repression_risk) AS mean_repression_risk,
    AVG(movement_outcome) AS mean_outcome
FROM collective_action_trials
GROUP BY institutional_response
ORDER BY mean_outcome DESC;

-- 5. Network support and participation.
SELECT
    CASE
        WHEN network_support < 3 THEN 'low_network_support'
        WHEN network_support < 7 THEN 'medium_network_support'
        ELSE 'high_network_support'
    END AS network_support_band,
    COUNT(*) AS n,
    AVG(action_participation) AS participation_rate,
    AVG(participation_intention) AS mean_intention,
    AVG(collective_efficacy) AS mean_efficacy
FROM collective_action_trials
GROUP BY network_support_band
ORDER BY participation_rate DESC;

-- 6. Repression risk and participation.
SELECT
    CASE
        WHEN perceived_repression_risk < 3 THEN 'low_risk'
        WHEN perceived_repression_risk < 7 THEN 'medium_risk'
        ELSE 'high_risk'
    END AS repression_risk_band,
    COUNT(*) AS n,
    AVG(action_participation) AS participation_rate,
    AVG(participation_cost) AS mean_cost,
    AVG(perceived_legitimacy) AS mean_legitimacy
FROM collective_action_trials
GROUP BY repression_risk_band
ORDER BY repression_risk_band;

-- 7. Join participant-level network exposure when network_edges are available.
SELECT
    t.participant,
    t.condition,
    t.identity_strength,
    t.perceived_injustice,
    t.collective_efficacy,
    COALESCE(n.observed_ties, 0) AS observed_ties,
    COALESCE(n.mean_tie_strength, 0) AS mean_tie_strength,
    t.participation_intention,
    t.action_participation
FROM collective_action_trials t
LEFT JOIN network_exposure n
    ON t.participant = n.participant
ORDER BY observed_ties DESC, participation_intention DESC;
