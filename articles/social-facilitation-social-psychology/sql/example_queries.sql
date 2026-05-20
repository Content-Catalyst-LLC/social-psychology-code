-- Example analytical queries for social facilitation research.

-- 1. Summary by condition and task domain.
SELECT
    condition,
    task_domain,
    n_trials,
    n_participants,
    mean_performance,
    mean_accuracy,
    mean_error_rate,
    mean_response_time,
    mean_arousal,
    mean_distraction,
    mean_evaluation,
    mean_task_difficulty,
    mean_task_mastery
FROM social_facilitation_summary
ORDER BY condition, task_domain;

-- 2. Audience effects by mastered versus difficult tasks.
SELECT
    predicted_pattern,
    COUNT(*) AS n,
    AVG(performance_score) AS mean_performance,
    AVG(accuracy) AS mean_accuracy,
    AVG(error_rate) AS mean_error_rate,
    AVG(arousal_index) AS mean_arousal,
    AVG(evaluation_apprehension_index) AS mean_evaluation_apprehension,
    AVG(distraction_conflict_index) AS mean_distraction_conflict
FROM facilitation_inhibition_cases
GROUP BY predicted_pattern
ORDER BY mean_performance DESC;

-- 3. Digital monitoring and performance.
SELECT
    digital_monitoring,
    condition,
    COUNT(*) AS n,
    AVG(performance_score) AS mean_performance,
    AVG(perceived_scrutiny) AS mean_scrutiny,
    AVG(evaluation_pressure) AS mean_evaluation,
    AVG(arousal_index) AS mean_arousal,
    AVG(error_rate) AS mean_error_rate
FROM social_facilitation_trials
GROUP BY digital_monitoring, condition
ORDER BY digital_monitoring, condition;

-- 4. Evaluation pressure by observer expertise and audience size.
SELECT
    condition,
    AVG(observer_expertise) AS mean_observer_expertise,
    AVG(audience_size) AS mean_audience_size,
    AVG(evaluation_pressure) AS mean_evaluation_pressure,
    AVG(perceived_scrutiny) AS mean_perceived_scrutiny,
    AVG(performance_score) AS mean_performance
FROM social_facilitation_trials
GROUP BY condition
ORDER BY mean_evaluation_pressure DESC;
