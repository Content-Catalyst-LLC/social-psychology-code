-- Example analytical queries for conformity and social influence research.

-- 1. Summary by condition and context.
SELECT
    condition,
    context,
    n_trials,
    n_participants,
    n_groups,
    conformity_rate,
    dissent_rate,
    mean_confidence_shift,
    mean_normative_influence,
    mean_informational_influence,
    mean_digital_social_proof,
    mean_response_time
FROM conformity_summary
ORDER BY conformity_rate DESC;

-- 2. Unanimity and visible dissent.
SELECT
    CASE
        WHEN visible_dissent < 3 THEN 'low_visible_dissent'
        WHEN visible_dissent < 7 THEN 'moderate_visible_dissent'
        ELSE 'high_visible_dissent'
    END AS dissent_band,
    COUNT(*) AS n,
    AVG(unanimity) AS mean_unanimity,
    AVG(conformed) AS conformity_rate,
    AVG(dissented) AS dissent_rate,
    AVG(confidence_shift) AS mean_confidence_shift
FROM conformity_trials
GROUP BY dissent_band
ORDER BY conformity_rate DESC;

-- 3. Public versus private responding.
SELECT
    public_response,
    private_response,
    COUNT(*) AS n,
    AVG(normative_pressure) AS mean_normative_pressure,
    AVG(conformed) AS conformity_rate,
    AVG(dissented) AS dissent_rate,
    AVG(response_time_ms) AS mean_response_time
FROM conformity_trials
GROUP BY public_response, private_response;

-- 4. Digital social proof.
SELECT
    CASE
        WHEN digital_social_proof_index < 3 THEN 'low_social_proof'
        WHEN digital_social_proof_index < 7 THEN 'moderate_social_proof'
        ELSE 'high_social_proof'
    END AS social_proof_band,
    COUNT(*) AS n,
    AVG(conformed) AS conformity_rate,
    AVG(confidence_shift) AS mean_confidence_shift,
    AVG(algorithmic_amplification) AS mean_algorithmic_amplification
FROM conformity_trials
GROUP BY social_proof_band
ORDER BY conformity_rate DESC;

-- 5. High-risk conformity audit.
SELECT
    condition,
    context,
    COUNT(*) AS n,
    AVG(normative_influence_index) AS mean_normative_influence,
    AVG(informational_influence_index) AS mean_informational_influence,
    AVG(digital_social_proof_index) AS mean_digital_social_proof,
    AVG(confidence_shift) AS mean_confidence_shift
FROM high_conformity_risk_cases
GROUP BY condition, context
ORDER BY n DESC;
