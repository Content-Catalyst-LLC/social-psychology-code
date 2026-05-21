-- Example analytical queries for obedience, authority, and social power research.

-- 1. Obedience by condition, institutional context, and escalation step.
SELECT
    condition,
    institution_context,
    escalation_step,
    n_trials,
    n_participants,
    obedience_rate,
    resistance_rate,
    protest_rate,
    mean_authority_pressure,
    mean_moral_resistance,
    mean_identification,
    mean_responsibility_after
FROM obedience_summary
ORDER BY condition, escalation_step;

-- 2. High-risk compliance under moral resistance.
SELECT
    condition,
    institution_context,
    COUNT(*) AS n,
    AVG(authority_pressure_index) AS mean_authority_pressure,
    AVG(moral_resistance_index) AS mean_moral_resistance,
    AVG(responsibility_displacement) AS mean_responsibility_displacement,
    AVG(moral_conflict) AS mean_moral_conflict,
    AVG(peer_dissent) AS mean_peer_dissent,
    AVG(hesitation) AS mean_hesitation,
    AVG(perceived_responsibility_after) AS mean_responsibility_after
FROM high_risk_obedience_cases
GROUP BY condition, institution_context
ORDER BY n DESC;

-- 3. Peer dissent and obedience.
SELECT
    CASE
        WHEN peer_dissent < 3 THEN 'low_peer_dissent'
        WHEN peer_dissent < 7 THEN 'moderate_peer_dissent'
        ELSE 'high_peer_dissent'
    END AS peer_dissent_band,
    COUNT(*) AS n,
    AVG(obeyed) AS obedience_rate,
    AVG(resisted) AS resistance_rate,
    AVG(protest) AS protest_rate,
    AVG(moral_conflict) AS mean_moral_conflict
FROM obedience_trials
GROUP BY peer_dissent_band
ORDER BY obedience_rate DESC;

-- 4. Responsibility displacement and perceived responsibility after action.
SELECT
    CASE
        WHEN responsibility_displacement < 3 THEN 'low_displacement'
        WHEN responsibility_displacement < 7 THEN 'moderate_displacement'
        ELSE 'high_displacement'
    END AS displacement_band,
    COUNT(*) AS n,
    AVG(obeyed) AS obedience_rate,
    AVG(perceived_responsibility_after) AS mean_responsibility_after,
    AVG(hesitation) AS mean_hesitation
FROM obedience_trials
GROUP BY displacement_band
ORDER BY obedience_rate DESC;

-- 5. Mission identification and obedience.
SELECT
    condition,
    AVG(mission_identification) AS mean_mission_identification,
    AVG(role_identification) AS mean_role_identification,
    AVG(authority_pressure_index) AS mean_authority_pressure,
    AVG(obeyed) AS obedience_rate,
    AVG(resisted) AS resistance_rate
FROM obedience_trials
GROUP BY condition
ORDER BY obedience_rate DESC;
