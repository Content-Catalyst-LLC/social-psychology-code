# Measurement Notes

## Contact quality composite

Q_i = mean(equal_status_i, common_goals_i, cooperation_i, institutional_support_i, voluntariness_i)

## Prejudice change

prejudice_change_i = prejudice_post_i - prejudice_pre_i

Negative values indicate reduced prejudice.

## Core model

Pr(reduced_prejudice_i = 1) =
logistic(beta0 + beta1 * contact_quality_i + beta2 * contact_frequency_i
         - beta3 * negative_contact_i - beta4 * anxiety_i
         + beta5 * empathy_i + beta6 * trust_i)

## Longitudinal anxiety update

anxiety_{t+1} = anxiety_t - beta * positive_contact_t + gamma * negative_contact_t

## Longitudinal empathy update

empathy_{t+1} = empathy_t + delta * positive_contact_t - rho * negative_contact_t

## Norm diffusion

inclusive_norm_{t+1} = inclusive_norm_t + lambda * cross_group_ties_t

## Mediation logic

contact_quality -> lower anxiety -> lower prejudice
contact_quality -> higher empathy -> lower prejudice
contact_quality -> higher trust -> lower social distance

## Recommended reliability checks

- Internal consistency for prejudice, anxiety, empathy, trust, threat, and social-distance scales
- Test-retest reliability for attitudes in longitudinal designs
- Site-level reliability for institutional support coding
- Intercoder reliability for qualitative contact-quality coding

## Recommended validity checks

- Distinguish contact quantity and quality
- Distinguish positive and negative contact
- Compare self-report attitude measures with behavioral or choice outcomes
- Test whether contact effects generalize beyond the specific individuals encountered
- Examine asymmetric effects by group status
- Check whether equal-status contact is actually perceived as equal by participants
