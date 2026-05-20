-- Example analytical queries for moral disengagement research.

-- 1. Summary by condition and domain.
SELECT
    condition,
    scenario_domain,
    n_trials,
    mean_md_index,
    harmful_rate,
    mean_policy_endorsement,
    mean_unethical_intention,
    mean_empathy,
    mean_guilt,
    mean_harm_visibility,
    mean_responsibility_clarity
FROM moral_disengagement_summary
ORDER BY condition, scenario_domain;

-- 2. Mechanism-specific means by condition.
SELECT
    condition,
    AVG(moral_justification) AS moral_justification,
    AVG(euphemistic_labeling) AS euphemistic_labeling,
    AVG(advantageous_comparison) AS advantageous_comparison,
    AVG(displaced_responsibility) AS displaced_responsibility,
    AVG(diffused_responsibility) AS diffused_responsibility,
    AVG(consequence_distortion) AS consequence_distortion,
    AVG(dehumanization) AS dehumanization,
    AVG(blame_attribution) AS blame_attribution,
    AVG(harmful_decision) AS harmful_rate
FROM moral_disengagement_trials
GROUP BY condition
ORDER BY condition;

-- 3. Harm visibility bands and harmful decisions.
SELECT
    CASE
        WHEN harm_visibility < 3 THEN 'low_visibility'
        WHEN harm_visibility < 7 THEN 'moderate_visibility'
        ELSE 'high_visibility'
    END AS harm_visibility_band,
    COUNT(*) AS n,
    AVG(md_index) AS mean_md_index,
    AVG(harmful_decision) AS harmful_rate,
    AVG(empathy) AS mean_empathy,
    AVG(guilt) AS mean_guilt
FROM moral_disengagement_trials
GROUP BY harm_visibility_band;

-- 4. Responsibility clarity and displacement/diffusion.
SELECT
    CASE
        WHEN responsibility_clarity < 3 THEN 'low_clarity'
        WHEN responsibility_clarity < 7 THEN 'moderate_clarity'
        ELSE 'high_clarity'
    END AS responsibility_clarity_band,
    COUNT(*) AS n,
    AVG(displaced_responsibility) AS mean_displacement,
    AVG(diffused_responsibility) AS mean_diffusion,
    AVG(perceived_agency) AS mean_agency,
    AVG(harmful_decision) AS harmful_rate
FROM moral_disengagement_trials
GROUP BY responsibility_clarity_band;
