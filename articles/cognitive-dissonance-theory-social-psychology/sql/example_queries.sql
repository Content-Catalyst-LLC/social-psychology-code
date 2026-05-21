-- Example analytical queries for cognitive dissonance research.

-- 1. Summary by paradigm, condition, and context.
SELECT
    paradigm,
    condition,
    institution_context,
    n_trials,
    n_participants,
    mean_attitude_change,
    mean_spreading,
    mean_outcome_value,
    mean_proselytizing,
    mean_coherence_pressure,
    mean_discomfort,
    mean_policy_reversal
FROM dissonance_summary
ORDER BY mean_discomfort DESC;

-- 2. Forced compliance: attitude change under high choice and low external justification.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(perceived_choice) AS mean_choice,
    AVG(external_justification) AS mean_external_justification,
    AVG(identity_threat) AS mean_identity_threat,
    AVG(attitude_change) AS mean_attitude_change
FROM dissonance_trials
WHERE paradigm = 'forced_compliance'
GROUP BY condition
ORDER BY mean_attitude_change DESC;

-- 3. Free choice: spreading of alternatives.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(chosen_post_value - chosen_pre_value) AS chosen_gain,
    AVG(rejected_post_value - rejected_pre_value) AS rejected_change,
    AVG(spreading_of_alternatives) AS mean_spread
FROM dissonance_trials
WHERE paradigm = 'free_choice'
GROUP BY condition
ORDER BY mean_spread DESC;

-- 4. Effort justification.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(effort_cost) AS mean_effort,
    AVG(outcome_value) AS mean_outcome_value,
    AVG(public_commitment) AS mean_public_commitment
FROM dissonance_trials
WHERE paradigm = 'effort_justification'
GROUP BY condition
ORDER BY mean_outcome_value DESC;

-- 5. Institutional escalation and policy reversal.
SELECT
    condition,
    institution_context,
    COUNT(*) AS n,
    AVG(sunk_cost) AS mean_sunk_cost,
    AVG(institutional_identity_threat) AS mean_identity_threat,
    AVG(evidence_strength) AS mean_evidence,
    AVG(accountability) AS mean_accountability,
    AVG(policy_reversal_willingness) AS mean_reversal_willingness
FROM dissonance_trials
WHERE paradigm = 'institutional_escalation'
GROUP BY condition, institution_context
ORDER BY mean_reversal_willingness ASC;
