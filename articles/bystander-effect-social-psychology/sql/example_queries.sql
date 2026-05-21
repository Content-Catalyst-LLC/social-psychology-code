-- Example analytical queries for bystander-effect research.

-- 1. Summary by condition and context.
SELECT
    condition,
    context_type,
    n_trials,
    n_participants,
    mean_perceived_bystanders,
    intervention_rate,
    mean_intervention_likelihood,
    mean_latency_ms,
    mean_felt_responsibility,
    mean_diffusion,
    mean_pluralistic_ignorance,
    mean_evaluation_apprehension,
    mean_emergency_clarity,
    mean_competence
FROM bystander_effect_summary
ORDER BY intervention_rate ASC;

-- 2. Direct responsibility assignment effects.
SELECT
    direct_assignment,
    leadership_cue,
    COUNT(*) AS n,
    AVG(felt_responsibility) AS mean_responsibility,
    AVG(diffusion_responsibility) AS mean_diffusion,
    AVG(intervention_likelihood) AS mean_likelihood,
    AVG(actual_intervention) AS intervention_rate,
    AVG(intervention_latency_ms) AS mean_latency
FROM bystander_effect_trials
GROUP BY direct_assignment, leadership_cue
ORDER BY intervention_rate DESC;

-- 3. High-risk nonintervention audit.
SELECT
    condition,
    context_type,
    COUNT(*) AS n,
    AVG(perceived_bystander_count) AS mean_bystanders,
    AVG(diffusion_responsibility) AS mean_diffusion,
    AVG(pluralistic_ignorance) AS mean_pluralistic_ignorance,
    AVG(evaluation_apprehension) AS mean_evaluation,
    AVG(perceived_competence) AS mean_competence,
    AVG(intervention_cost) AS mean_cost
FROM high_risk_nonintervention_cases
GROUP BY condition, context_type
ORDER BY n DESC;

-- 4. Online bystander behavior.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(perceived_bystander_count) AS mean_visible_audience,
    AVG(platform_traceability) AS mean_traceability,
    AVG(moderation_visibility) AS mean_moderation_visibility,
    AVG(intervention_norm_salience) AS mean_norm_salience,
    AVG(actual_intervention) AS intervention_rate
FROM bystander_effect_trials
WHERE online_context = 1
GROUP BY condition
ORDER BY intervention_rate DESC;
