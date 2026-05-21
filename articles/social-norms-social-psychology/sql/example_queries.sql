-- Example analytical queries for social-norms research.

-- 1. Summary by condition, policy domain, and message type.
SELECT
    condition,
    policy_domain,
    message_type,
    n_trials,
    n_participants,
    compliance_rate,
    reporting_rate,
    mean_intention,
    mean_contribution,
    mean_descriptive_norm,
    mean_injunctive_norm,
    mean_empirical_expectation,
    mean_normative_expectation,
    mean_pluralistic_ignorance,
    mean_norm_strength,
    mean_enforcement,
    mean_legitimacy_trust,
    mean_tipping_margin
FROM social_norms_summary
ORDER BY compliance_rate DESC;

-- 2. Descriptive versus injunctive message comparison.
SELECT
    message_type,
    COUNT(*) AS n,
    AVG(descriptive_norm) AS mean_descriptive,
    AVG(injunctive_norm) AS mean_injunctive,
    AVG(complied) AS compliance_rate,
    AVG(compliance_intention) AS mean_intention,
    AVG(post_message_norm_perception) AS mean_post_message_norm
FROM social_norms_trials
WHERE message_type IN ('descriptive', 'injunctive', 'combined', 'dynamic', 'correction')
GROUP BY message_type
ORDER BY compliance_rate DESC;

-- 3. Pluralistic ignorance audit.
SELECT
    policy_domain,
    reference_group,
    COUNT(*) AS n,
    AVG(personal_attitude) AS mean_private_attitude,
    AVG(injunctive_norm) AS mean_perceived_group_approval,
    AVG(pluralistic_ignorance) AS mean_pluralistic_ignorance,
    AVG(complied) AS compliance_rate,
    AVG(compliance_intention) AS mean_intention
FROM pluralistic_ignorance_cases
GROUP BY policy_domain, reference_group
ORDER BY mean_pluralistic_ignorance DESC;

-- 4. Legitimacy and compliance.
SELECT
    CASE
        WHEN institutional_legitimacy < 3 THEN 'low_legitimacy'
        WHEN institutional_legitimacy < 7 THEN 'moderate_legitimacy'
        ELSE 'high_legitimacy'
    END AS legitimacy_band,
    COUNT(*) AS n,
    AVG(trust_in_institution) AS mean_trust,
    AVG(complied) AS compliance_rate,
    AVG(contribution_amount) AS mean_contribution,
    AVG(reported_violation) AS reporting_rate
FROM social_norms_trials
GROUP BY legitimacy_band
ORDER BY compliance_rate DESC;

-- 5. Threshold/tipping dynamics.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(norm_threshold) AS mean_threshold,
    AVG(tipping_exposure) AS mean_tipping_exposure,
    AVG(tipping_margin) AS mean_tipping_margin,
    AVG(complied) AS compliance_rate
FROM social_norms_trials
GROUP BY condition
ORDER BY mean_tipping_margin DESC;
