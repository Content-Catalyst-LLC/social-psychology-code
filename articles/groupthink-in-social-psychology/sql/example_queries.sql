-- Example analytical queries for groupthink research.

-- 1. Summary by condition and institutional context.
SELECT
    condition,
    institution_context,
    n_trials,
    n_participants,
    n_groups,
    mean_groupthink_risk,
    mean_antecedent_risk,
    mean_symptoms,
    mean_process_quality,
    mean_safeguards,
    mean_unanimity_gap,
    mean_decision_quality,
    mean_forecast_calibration,
    mean_implementation_risk,
    mean_review_quality
FROM groupthink_summary
ORDER BY mean_groupthink_risk DESC;

-- 2. High-risk groupthink audit.
SELECT
    condition,
    institution_context,
    COUNT(*) AS n,
    AVG(antecedent_risk_index) AS mean_antecedent_risk,
    AVG(symptom_index) AS mean_symptoms,
    AVG(process_quality_index) AS mean_process_quality,
    AVG(safeguard_index) AS mean_safeguards,
    AVG(unanimity_gap) AS mean_unanimity_gap,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(implementation_risk) AS mean_implementation_risk
FROM high_risk_groupthink_cases
GROUP BY condition, institution_context
ORDER BY mean_groupthink_risk DESC;

-- 3. Safeguards and decision quality.
SELECT
    CASE
        WHEN safeguard_index < 3 THEN 'weak_safeguards'
        WHEN safeguard_index < 7 THEN 'moderate_safeguards'
        ELSE 'strong_safeguards'
    END AS safeguard_band,
    COUNT(*) AS n,
    AVG(self_censorship) AS mean_self_censorship,
    AVG(unanimity_gap) AS mean_unanimity_gap,
    AVG(decision_quality) AS mean_decision_quality,
    AVG(forecast_calibration) AS mean_forecast_calibration,
    AVG(implementation_risk) AS mean_implementation_risk
FROM groupthink_trials
GROUP BY safeguard_band
ORDER BY mean_decision_quality DESC;

-- 4. Leadership directiveness and self-censorship.
SELECT
    CASE
        WHEN leadership_directive < 3 THEN 'low_directiveness'
        WHEN leadership_directive < 7 THEN 'moderate_directiveness'
        ELSE 'high_directiveness'
    END AS leadership_band,
    COUNT(*) AS n,
    AVG(cohesion) AS mean_cohesion,
    AVG(consensus_pressure) AS mean_consensus_pressure,
    AVG(self_censorship) AS mean_self_censorship,
    AVG(dissent_visibility) AS mean_dissent_visibility,
    AVG(decision_quality) AS mean_decision_quality
FROM groupthink_trials
GROUP BY leadership_band
ORDER BY mean_self_censorship DESC;

-- 5. False unanimity.
SELECT
    condition,
    institution_context,
    AVG(perceived_unanimity) AS mean_perceived_unanimity,
    AVG(private_disagreement) AS mean_private_disagreement,
    AVG(unanimity_gap) AS mean_unanimity_gap,
    AVG(self_censorship) AS mean_self_censorship,
    AVG(decision_quality) AS mean_decision_quality
FROM groupthink_trials
GROUP BY condition, institution_context
ORDER BY mean_unanimity_gap DESC;
