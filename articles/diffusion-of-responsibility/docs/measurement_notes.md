# Measurement Notes

## Felt responsibility

A simple inverse model:

R_f = 1 / n

where n is the perceived number of possible responders.

A more realistic model:

R_f = RoleClarity + AccountabilityAssignment + SocialVisibility
      - log(1 + BystanderCount) - Ambiguity - EvaluationApprehension

## Pluralistic ignorance gap

PIG_i = PrivateConcern_i - PerceivedGroupConcern_i

Positive values indicate private concern exceeding perceived group concern.

## Intervention propensity

P(Intervention_i = 1) = logit^-1(beta0
    + beta1*FeltResponsibility_i
    + beta2*RoleClarity_i
    + beta3*InterventionEfficacy_i
    + beta4*PrivateConcern_i
    - beta5*Ambiguity_i
    - beta6*EvaluationApprehension_i
    - beta7*BystanderCount_i)

## Organizational accountability fragmentation

UnitResponsibility_i = Accountability_i / k

where k is the number of units or roles across which responsibility is distributed, unless responsibility is explicitly assigned.

## Institutional inaction normalization

InactionNorm_{t+1} = InactionNorm_t
                    + eta1*Fragmentation_t
                    + eta2*Ambiguity_t
                    - eta3*AccountabilityClarity_t
                    - eta4*LeadershipCue_t

## Recommended reliability checks

- Role clarity scale reliability
- Private concern and perceived group concern reliability
- Evaluation apprehension scale reliability
- Intervention efficacy scale reliability
- Response-time filtering rules
- Measurement invariance across emergency and organizational contexts

## Recommended validity checks

- Compare actual and perceived bystander count.
- Distinguish emergency ambiguity from responsibility ambiguity.
- Test whether direct appeals increase personal responsibility.
- Test whether role assignment reduces response delay.
- Test whether bystander effects weaken in dangerous emergencies.
- Test whether social visibility increases helping.
- Test whether organizational fragmentation predicts reporting failure.
