-- Example analytical queries for deindividuation research.

-- 1. Summary by condition and context.
SELECT
    condition,
    context_type,
    n_trials,
    n_participants,
    mean_behavior,
    mean_prosocial,
    mean_antisocial,
    mean_anonymity,
    mean_self_awareness,
    mean_accountability,
    mean_group_identity,
    mean_norm_congruence,
    mean_deindividuation
FROM deindividuation_summary
ORDER BY condition, context_type;

-- 2. SIDE-relevant norm-congruent behavior.
SELECT
    condition,
    norm_valence_band,
    COUNT(*) AS n,
    AVG(anonymity) AS mean_anonymity,
    AVG(group_identity_salience) AS mean_group_identity,
    AVG(side_norm_activation) AS mean_side_norm_activation,
    AVG(norm_congruence) AS mean_norm_congruence,
    AVG(prosocial_behavior) AS mean_prosocial,
    AVG(antisocial_behavior) AS mean_antisocial
FROM side_model_cases
GROUP BY condition, norm_valence_band
ORDER BY condition, norm_valence_band;

-- 3. Online/platform accountability and antisocial behavior.
SELECT
    condition,
    context_type,
    COUNT(*) AS n,
    AVG(anonymity) AS mean_anonymity,
    AVG(accountability) AS mean_accountability,
    AVG(moderation_visibility) AS mean_moderation_visibility,
    AVG(perceived_surveillance) AS mean_surveillance,
    AVG(antisocial_behavior) AS mean_antisocial
FROM deindividuation_trials
WHERE context_type IN ('online', 'platform')
GROUP BY condition, context_type
ORDER BY mean_antisocial DESC;

-- 4. Identity shift and responsibility diffusion.
SELECT
    condition,
    AVG(identity_shift_index) AS mean_identity_shift,
    AVG(responsibility_diffusion) AS mean_responsibility_diffusion,
    AVG(moral_disengagement) AS mean_moral_disengagement,
    AVG(self_awareness) AS mean_self_awareness,
    AVG(accountability) AS mean_accountability
FROM deindividuation_trials
GROUP BY condition
ORDER BY mean_identity_shift DESC;
