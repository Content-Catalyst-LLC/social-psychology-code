-- Example analytical queries for heuristics-and-biases research.

-- 1. Summary by heuristic, condition, context, and domain.
SELECT
    heuristic_type,
    condition,
    institution_context,
    judgment_domain,
    n_trials,
    n_participants,
    mean_anchoring_error,
    mean_absolute_error,
    mean_calibration_error,
    mean_overconfidence,
    mean_decision_quality,
    mean_evidence_discipline
FROM heuristics_biases_summary
ORDER BY mean_decision_quality ASC;

-- 2. Anchoring by condition.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(anchor_value) AS mean_anchor,
    AVG(true_value) AS mean_true_value,
    AVG(estimate) AS mean_estimate,
    AVG(anchoring_error) AS mean_anchoring_error,
    AVG(absolute_error) AS mean_absolute_error
FROM heuristics_biases_trials
WHERE heuristic_type = 'anchoring'
GROUP BY condition
ORDER BY mean_absolute_error DESC;

-- 3. Calibration and overconfidence.
SELECT
    heuristic_type,
    condition,
    COUNT(*) AS n,
    AVG(confidence_rating) AS mean_confidence,
    AVG(actual_accuracy) AS mean_accuracy,
    AVG(calibration_error) AS mean_calibration_error,
    AVG(overconfidence_score) AS mean_overconfidence
FROM heuristics_biases_trials
GROUP BY heuristic_type, condition
ORDER BY mean_calibration_error DESC;

-- 4. Affect heuristic: risk-benefit coupling.
SELECT
    condition,
    frame_type,
    COUNT(*) AS n,
    AVG(affect_valence) AS mean_affect,
    AVG(perceived_risk) AS mean_risk,
    AVG(perceived_benefit) AS mean_benefit
FROM heuristics_biases_trials
WHERE heuristic_type IN ('affect', 'framing', 'mixed')
GROUP BY condition, frame_type
ORDER BY mean_risk DESC;

-- 5. Debiasing and decision quality.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(debiasing_intervention_strength) AS mean_debiasing,
    AVG(institutional_accountability) AS mean_accountability,
    AVG(feedback_quality) AS mean_feedback,
    AVG(disconfirming_evidence_exposure) AS mean_disconfirming_exposure,
    AVG(decision_quality) AS mean_decision_quality
FROM heuristics_biases_trials
GROUP BY condition
ORDER BY mean_decision_quality DESC;
