-- Example analytical queries for fundamental attribution error research.

-- 1. Summary by condition and behavior valence.
SELECT
    condition,
    behavior_valence,
    n_trials,
    mean_dispositional,
    mean_situational,
    mean_fae_score,
    mean_constraint_neglect,
    mean_correspondence_bias,
    mean_blame,
    mean_punishment
FROM attribution_summary
ORDER BY condition, behavior_valence;

-- 2. High-constraint cases where observers still infer disposition.
SELECT
    condition,
    actor_role,
    observer_role,
    COUNT(*) AS n,
    AVG(dispositional_attribution) AS mean_dispositional,
    AVG(situational_attribution) AS mean_situational,
    AVG(constraint_neglect) AS mean_constraint_neglect,
    AVG(moral_blame) AS mean_blame,
    AVG(punishment_recommendation) AS mean_punishment
FROM attribution_trials
WHERE actual_constraint >= 7
GROUP BY condition, actor_role, observer_role;

-- 3. Accountability bands and FAE scores.
SELECT
    CASE
        WHEN accountability_pressure < 3 THEN 'low_accountability'
        WHEN accountability_pressure < 7 THEN 'moderate_accountability'
        ELSE 'high_accountability'
    END AS accountability_band,
    COUNT(*) AS n,
    AVG(fae_score) AS mean_fae_score,
    AVG(constraint_neglect) AS mean_constraint_neglect,
    AVG(dispositional_attribution) AS mean_dispositional,
    AVG(situational_attribution) AS mean_situational
FROM attribution_trials
GROUP BY accountability_band
ORDER BY accountability_band;

-- 4. Cognitive load and correction.
SELECT
    CASE
        WHEN cognitive_load < 3 THEN 'low_load'
        WHEN cognitive_load < 7 THEN 'moderate_load'
        ELSE 'high_load'
    END AS cognitive_load_band,
    COUNT(*) AS n,
    AVG(dispositional_attribution) AS mean_dispositional,
    AVG(situational_attribution) AS mean_situational,
    AVG(fae_score) AS mean_fae_score,
    AVG(perspective_taking) AS mean_perspective_taking
FROM attribution_trials
GROUP BY cognitive_load_band;
