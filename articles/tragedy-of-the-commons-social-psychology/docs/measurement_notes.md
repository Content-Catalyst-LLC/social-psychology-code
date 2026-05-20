# Measurement Notes

## Commons stock dynamics

R_{t+1} = R_t + g(R_t) - sum(x_i,t)

where:

- R_t = resource stock at time t
- g(R_t) = regeneration function
- x_i,t = extraction by actor i at time t

## Regeneration model

A simple logistic regeneration function:

g(R_t) = r R_t (1 - R_t / K)

where:

- r = intrinsic regeneration rate
- K = carrying capacity

## Unsustainable extraction

sum(x_i,t) > g(R_t)

Resource stock declines when total extraction exceeds regeneration.

## Individual utility

u_i = b(x_i) - s_i - lambda_i * D_t

where:

- b(x_i) = private benefit from extraction
- s_i = expected sanction
- D_t = depletion risk or collective damage
- lambda_i = degree to which actor internalizes collective damage

## Expected sanction

s_i = Monitoring_i * SanctionProbability_i * SanctionSeverity_i

## Institutional effectiveness

InstitutionalEffect_i =
  BoundaryClarity_i
  * MonitoringCredibility_i
  * SanctionCredibility_i
  * Legitimacy_i
  * RuleParticipation_i

## Cooperative restraint probability

P(Restraint_i = 1) = logit^-1(beta0
    + beta1*Trust_i
    + beta2*Legitimacy_i
    + beta3*Monitoring_i
    + beta4*StewardshipNorm_i
    + beta5*ReciprocityExpectation_i
    + beta6*LocalKnowledge_i
    - beta7*ExtractionTemptation_i
    - beta8*Asymmetry_i)

## Recommended reliability checks

- Legitimacy scale reliability
- Trust scale reliability
- Stewardship norm scale reliability
- Fairness scale reliability
- Local ecological knowledge scale reliability
- Comprehension checks for resource dynamics
- Response-time filtering rules

## Recommended validity checks

- Verify resource dynamics and sustainability thresholds.
- Distinguish open-access from governed common property.
- Compare imposed rules with user-participatory rules.
- Test whether sanctions depend on legitimacy.
- Test whether boundary clarity reduces extraction.
- Test whether asymmetry weakens perceived fairness and restraint.
- Test whether local ecological knowledge improves extraction discipline.
