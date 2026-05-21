-- Summary by condition, task type, and remote status.
SELECT * FROM social_loafing_summary
ORDER BY mean_effort_loss DESC;

-- Compare pooled, identifiable, and traceable digital teams.
SELECT
    condition,
    COUNT(*) AS n,
    AVG(group_size) AS mean_group_size,
    AVG(effort_loss) AS mean_effort_loss,
    AVG(motivation_loss) AS mean_motivation_loss,
    AVG(identifiability) AS mean_identifiability,
    AVG(accountability) AS mean_accountability,
    AVG(digital_traceability) AS mean_digital_traceability
FROM social_loafing_trials
WHERE condition IN ('pooled_group', 'identifiable_group', 'traceable_digital_team')
GROUP BY condition
ORDER BY mean_effort_loss DESC;

-- High-loafing audit cases.
SELECT
    participant,
    team_id,
    condition,
    task_type,
    group_size,
    effort_loss,
    motivation_loss,
    identifiability,
    accountability,
    free_rider_expectation,
    sucker_effect_concern
FROM social_loafing_trials
WHERE effort_loss >= 15 OR motivation_loss >= 15
ORDER BY effort_loss DESC;
