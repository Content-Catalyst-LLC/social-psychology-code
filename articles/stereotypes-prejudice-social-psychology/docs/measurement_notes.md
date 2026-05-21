# Measurement Notes

## Stereotype association

A(g, a) represents the strength of association between group g and attribute a.

## Illusory correlation

IC = P_hat(a | g) - P(a | g)

A positive value means the perceived group-attribute association exceeds the observed association.

## Stereotype content

Warmth and competence can be modeled as outcomes of perceived competition and perceived status:

Warmth = beta0 - beta1*Competition + error
Competence = gamma0 + gamma1*Status + error

## Prejudice model

Prejudice = alpha0
  + alpha1*StereotypeStrength
  + alpha2*PerceivedThreat
  + alpha3*SocialNorms
  - alpha4*ContactQuality
  + error

## Discrimination model

DiscriminationTendency = logit^-1(
  beta0
+ beta1*Prejudice
+ beta2*StereotypeStrength
+ beta3*ImplicitScore
+ beta4*Threat
- beta5*StructuredCriteria
- beta6*Accountability
)

## Stereotype threat model

PerformanceObserved = BaselinePerformance
  - delta*StereotypeThreatSalience
  - lambda*WorkingMemoryLoad
  + theta*IdentitySafety
  + error

## Institutional accumulation

Inequality_next = Inequality_current + sum(decision_disparity_k)

Small group-based decision differences can become consequential when repeated across many evaluative systems.

## Recommended validity checks

- Confirm threat-salience manipulation changes perceived threat.
- Confirm contact-quality measures distinguish cooperative contact from superficial exposure.
- Confirm stereotype-threat manipulation changes threat salience without unnecessary harm.
- Test whether structured criteria reduce discriminatory tendency.
- Test whether perceived status predicts competence and competition predicts warmth.
- Test whether implicit scores add predictive information beyond explicit prejudice.
