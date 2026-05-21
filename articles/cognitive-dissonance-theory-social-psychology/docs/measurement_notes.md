# Measurement Notes

## Dissonance magnitude

Delta = weighted_dissonant_cognitions / (weighted_consonant_cognitions + weighted_dissonant_cognitions)

## Motivation to reduce dissonance

M = f(Delta, perceived_responsibility, identity_relevance, public_commitment)

## Attitude change

AttitudeChange = PostAttitude - PreAttitude

## Post-decision spreading of alternatives

Spread = (ChosenPost - ChosenPre) - (RejectedPost - RejectedPre)

## Forced compliance model

AttitudeChange = beta0
  + beta1*CounterAttitudinalBehavior
  + beta2*PerceivedChoice
  + beta3*IdentityThreat
  - beta4*ExternalJustification
  - beta5*SelfAffirmation
  + error

## Effort justification model

OutcomeValue = alpha0
  + alpha1*EffortCost
  + alpha2*Commitment
  + alpha3*PublicCommitment
  + error

## Institutional rationalization model

PolicyReversalWillingness = logit^-1(
  beta0
- beta1*SunkCost
- beta2*PublicCommitment
- beta3*InstitutionalIdentityThreat
+ beta4*EvidenceStrength
+ beta5*Accountability
)

## Recommended validity checks

- Confirm that dissonance induction changes discomfort or tension.
- Confirm that perceived choice differs by condition.
- Confirm that effort cost differs across initiation conditions.
- Confirm that self-affirmation reduces defensive attitude change where predicted.
- Test whether public commitment increases rationalization.
- Test whether high external justification reduces dissonance-related attitude change.
- Compare cognitive dissonance predictions with self-perception or impression-management alternatives.
