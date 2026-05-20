-- Example analytical queries for self-serving bias research.

-- 1. Attribution pattern by valence and self/other condition.
SELECT
    condition,
    outcome_valence,
    self_other,
    n_trials,
    mean_internal,
    mean_external,
    mean_responsibility,
    mean_credit,
    mean_excuse,
    mean_learning
FROM attribution_summary
ORDER BY condition, self_other, outcome_valence;

-- 2. Self-serving bias score by condition.
SELECT
    pos.condition,
    pos.self_other,
    pos.mean_internal - neg.mean_internal AS internal_success_failure_gap,
    neg.mean_external - pos.mean_external AS external_failure_success_gap,
    (pos.mean_internal - neg.mean_internal) + (neg.mean_external - pos.mean_external) AS full_ssb_score
FROM attribution_summary pos
JOIN attribution_summary neg
    ON pos.condition = neg.condition
   AND pos.self_other = neg.self_other
WHERE pos.outcome_valence = 'positive'
  AND neg.outcome_valence = 'negative'
ORDER BY full_ssb_score DESC;

-- 3. Accountability bands and deflection.
SELECT
    CASE
        WHEN accountability_pressure < 3 THEN 'low_accountability'
        WHEN accountability_pressure < 7 THEN 'moderate_accountability'
        ELSE 'high_accountability'
    END AS accountability_band,
    COUNT(*) AS n,
    AVG(internal_attribution) AS mean_internal,
    AVG(external_attribution) AS mean_external,
    AVG(excuse_making) AS mean_excuse,
    AVG(learning_intention) AS mean_learning
FROM self_serving_bias_trials
WHERE outcome_valence = 'negative'
  AND self_other = 'self'
GROUP BY accountability_band
ORDER BY accountability_band;

-- 4. Evidence strength and attribution.
SELECT
    CASE
        WHEN evidence_strength < 3 THEN 'low_evidence'
        WHEN evidence_strength < 7 THEN 'moderate_evidence'
        ELSE 'high_evidence'
    END AS evidence_band,
    outcome_valence,
    self_other,
    COUNT(*) AS n,
    AVG(internal_attribution) AS mean_internal,
    AVG(external_attribution) AS mean_external,
    AVG(responsibility_rating) AS mean_responsibility,
    AVG(learning_intention) AS mean_learning
FROM self_serving_bias_trials
GROUP BY evidence_band, outcome_valence, self_other;
