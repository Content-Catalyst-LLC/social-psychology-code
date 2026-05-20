-- Example analytical queries for contact hypothesis research.

-- 1. Contact condition summary.
SELECT
    condition,
    n_trials,
    n_participants,
    mean_contact_quality,
    mean_allport_quality,
    mean_negative_contact,
    mean_anxiety,
    mean_empathy,
    mean_trust,
    mean_prejudice_change
FROM condition_summary
ORDER BY mean_prejudice_change ASC;

-- 2. Contact quality bands and prejudice change.
SELECT
    CASE
        WHEN contact_quality < 3 THEN 'low_quality'
        WHEN contact_quality < 7 THEN 'medium_quality'
        ELSE 'high_quality'
    END AS contact_quality_band,
    COUNT(*) AS n,
    AVG(prejudice_change) AS mean_prejudice_change,
    AVG(intergroup_anxiety) AS mean_anxiety,
    AVG(empathy) AS mean_empathy,
    AVG(trust) AS mean_trust
FROM contact_trials
GROUP BY contact_quality_band
ORDER BY mean_prejudice_change ASC;

-- 3. Positive and negative contact comparison.
SELECT
    CASE
        WHEN negative_contact >= 7 THEN 'high_negative_contact'
        WHEN contact_quality >= 7 THEN 'high_positive_contact'
        ELSE 'mixed_or_moderate_contact'
    END AS contact_valence_type,
    COUNT(*) AS n,
    AVG(prejudice_change) AS mean_prejudice_change,
    AVG(social_distance) AS mean_social_distance,
    AVG(future_contact_willingness) AS mean_future_contact
FROM contact_trials
GROUP BY contact_valence_type;

-- 4. Group-status asymmetry.
SELECT
    group_status,
    condition,
    COUNT(*) AS n,
    AVG(prejudice_change) AS mean_prejudice_change,
    AVG(negative_contact) AS mean_negative_contact,
    AVG(allport_quality) AS mean_allport_quality
FROM contact_trials
GROUP BY group_status, condition
ORDER BY group_status, mean_prejudice_change ASC;

-- 5. Site-level institutional support.
SELECT
    site_id,
    COUNT(*) AS n,
    AVG(institutional_support) AS mean_institutional_support,
    AVG(contact_quality) AS mean_contact_quality,
    AVG(prejudice_change) AS mean_prejudice_change,
    AVG(inclusive_norm_perception) AS mean_inclusive_norm
FROM contact_trials
GROUP BY site_id
ORDER BY mean_institutional_support DESC;
