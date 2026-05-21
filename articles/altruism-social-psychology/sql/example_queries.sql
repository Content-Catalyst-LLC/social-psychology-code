-- Example analytical queries for altruism research.

-- 1. Summary by condition and context.
SELECT
    condition,
    context_type,
    n_trials,
    n_participants,
    altruism_rate,
    punishment_rate,
    mean_donation,
    mean_volunteer_minutes,
    mean_public_goods_contribution,
    mean_empathy,
    mean_helping_cost,
    mean_recipient_need,
    mean_identity_overlap,
    mean_moral_identity,
    mean_efficacy,
    mean_other_regarding_weight,
    mean_egoistic_reward
FROM altruism_summary
ORDER BY altruism_rate DESC;

-- 2. Empathy and cost bands.
SELECT
    condition,
    CASE
        WHEN helping_cost < 2.5 THEN 'low_cost'
        WHEN helping_cost < 5.0 THEN 'moderate_cost'
        WHEN helping_cost < 7.5 THEN 'high_cost'
        ELSE 'very_high_cost'
    END AS cost_band,
    COUNT(*) AS n,
    AVG(empathy_score) AS mean_empathy,
    AVG(altruistic_decision) AS altruism_rate,
    AVG(donation_amount) AS mean_donation,
    AVG(perceived_efficacy) AS mean_efficacy
FROM altruism_trials
GROUP BY condition, cost_band
ORDER BY condition, cost_band;

-- 3. Anonymous versus public helping.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(reputation_visibility) AS mean_reputation_visibility,
    AVG(warm_glow_expectation) AS mean_warm_glow,
    AVG(reciprocity_expectation) AS mean_reciprocity,
    AVG(altruistic_decision) AS altruism_rate,
    AVG(donation_amount) AS mean_donation
FROM altruism_trials
WHERE condition IN ('anonymous_helping', 'public_helping')
GROUP BY condition;

-- 4. High-cost helping audit.
SELECT
    condition,
    context_type,
    COUNT(*) AS n,
    AVG(empathy_score) AS mean_empathy,
    AVG(helping_cost) AS mean_cost,
    AVG(moral_identity) AS mean_moral_identity,
    AVG(perceived_efficacy) AS mean_efficacy,
    AVG(donation_amount) AS mean_donation,
    AVG(time_volunteered_minutes) AS mean_volunteer_minutes
FROM high_cost_helping_cases
GROUP BY condition, context_type
ORDER BY n DESC;

-- 5. Altruistic punishment and public goods.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(social_norm_salience) AS mean_norm_salience,
    AVG(moral_identity) AS mean_moral_identity,
    AVG(altruistic_punishment) AS punishment_rate,
    AVG(punishment_cost) AS mean_punishment_cost,
    AVG(public_goods_contribution) AS mean_public_goods_contribution
FROM altruism_trials
WHERE condition IN ('public_goods', 'altruistic_punishment')
GROUP BY condition;
