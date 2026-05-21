-- Example analytical queries for prosocial behavior research.

-- 1. Summary by condition and context.
SELECT
    condition,
    context_type,
    n_trials,
    n_participants,
    helping_rate,
    emotional_support_rate,
    mean_donation,
    mean_volunteer_minutes,
    mean_cooperation_contribution,
    mean_empathy,
    mean_norm_salience,
    mean_efficacy,
    mean_helping_cost,
    mean_bystander_count,
    mean_felt_responsibility,
    mean_institutional_legitimacy
FROM prosocial_behavior_summary
ORDER BY helping_rate DESC;

-- 2. Helping by cost band.
SELECT
    condition,
    CASE
        WHEN helping_cost < 2.5 THEN 'low_cost'
        WHEN helping_cost < 5.0 THEN 'moderate_cost'
        WHEN helping_cost < 7.5 THEN 'high_cost'
        ELSE 'very_high_cost'
    END AS cost_band,
    COUNT(*) AS n,
    AVG(helping_decision) AS helping_rate,
    AVG(donation_amount) AS mean_donation,
    AVG(cooperation_contribution) AS mean_cooperation,
    AVG(efficacy_belief) AS mean_efficacy,
    AVG(felt_responsibility) AS mean_responsibility
FROM prosocial_behavior_trials
GROUP BY condition, cost_band
ORDER BY condition, cost_band;

-- 3. Institutional legitimacy and public cooperation.
SELECT
    context_type,
    COUNT(*) AS n,
    AVG(institutional_legitimacy) AS mean_legitimacy,
    AVG(trust_level) AS mean_trust,
    AVG(norm_salience) AS mean_norms,
    AVG(efficacy_belief) AS mean_efficacy,
    AVG(helping_decision) AS helping_rate,
    AVG(cooperation_contribution) AS mean_cooperation
FROM prosocial_behavior_trials
WHERE context_type IN ('public_health', 'public_goods', 'organization')
GROUP BY context_type
ORDER BY mean_cooperation DESC;

-- 4. Bystander suppression.
SELECT
    CASE
        WHEN bystander_count = 0 THEN 'alone'
        WHEN bystander_count <= 3 THEN 'small_group'
        WHEN bystander_count <= 10 THEN 'medium_group'
        ELSE 'large_group'
    END AS bystander_band,
    COUNT(*) AS n,
    AVG(felt_responsibility) AS mean_responsibility,
    AVG(helping_decision) AS helping_rate,
    AVG(response_time_ms) AS mean_response_time
FROM prosocial_behavior_trials
GROUP BY bystander_band
ORDER BY mean_responsibility DESC;
