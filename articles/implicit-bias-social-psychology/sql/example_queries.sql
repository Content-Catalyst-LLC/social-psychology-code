-- Example analytical queries for implicit-bias research.

-- 1. Trial summary by condition, context, and congruent/incongruent block.
SELECT
    condition,
    institution_context,
    congruent_block,
    n_trials,
    n_participants,
    mean_response_time,
    accuracy_rate,
    mean_explicit_attitude,
    mean_judgment,
    mean_behavioral_outcome,
    mean_automaticity_risk,
    mean_mitigation
FROM implicit_bias_summary
ORDER BY condition, institution_context, congruent_block;

-- 2. Simple participant-level latency difference.
SELECT
    participant,
    condition,
    mean_incongruent_rt,
    mean_congruent_rt,
    (mean_incongruent_rt - mean_congruent_rt) AS simple_latency_difference,
    mean_explicit_attitude,
    mean_judgment,
    mean_behavioral_outcome
FROM participant_latency_blocks
WHERE mean_incongruent_rt IS NOT NULL
  AND mean_congruent_rt IS NOT NULL
ORDER BY simple_latency_difference DESC;

-- 3. Mitigation conditions and behavioral outcomes.
SELECT
    condition,
    institution_context,
    COUNT(*) AS n,
    AVG(mitigation_index) AS mean_mitigation,
    AVG(automaticity_risk_index) AS mean_automaticity_risk,
    AVG(judgment_score) AS mean_judgment,
    AVG(behavioral_outcome) AS mean_behavioral_outcome
FROM implicit_bias_trials
GROUP BY condition, institution_context
ORDER BY mean_mitigation DESC;

-- 4. High automaticity-risk cases.
SELECT
    condition,
    institution_context,
    COUNT(*) AS n,
    AVG(cognitive_load) AS mean_cognitive_load,
    AVG(time_pressure) AS mean_time_pressure,
    AVG(accountability) AS mean_accountability,
    AVG(structured_decision_support) AS mean_structured_support,
    AVG(judgment_score) AS mean_judgment,
    AVG(behavioral_outcome) AS mean_behavioral_outcome
FROM implicit_bias_trials
WHERE automaticity_risk_index > 2
GROUP BY condition, institution_context;

-- 5. Follow-up durability.
SELECT
    condition,
    followup_days,
    COUNT(*) AS n,
    AVG(response_time_ms) AS mean_rt,
    AVG(judgment_score) AS mean_judgment,
    AVG(behavioral_outcome) AS mean_behavioral_outcome
FROM implicit_bias_trials
WHERE followup_days > 0
GROUP BY condition, followup_days
ORDER BY followup_days;
