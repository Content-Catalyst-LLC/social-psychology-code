# Measurement Notes

## Conformity probability

A practical model can estimate conformity as:

P(Conformity) = logit^-1(
  beta0
+ beta1*Ambiguity
+ beta2*NormativePressure
+ beta3*InformationalUncertainty
+ beta4*Unanimity
+ beta5*Cohesion
+ beta6*StatusStrength
+ beta7*PublicResponse
+ beta8*GroupIdentification
- beta9*VisibleDissent
- beta10*PrivateResponse
)

## Norm adoption

A simple judgment-update model:

J_next = (1 - lambda) * PrivateJudgment + lambda * GroupConsensus

where lambda is susceptibility to social influence.

## Dissent effect

Visible dissent should reduce conformity through two pathways:

1. It weakens perceived unanimity.
2. It reduces social isolation for independent judgment.

## Digital social proof

Social proof can be modeled as visible aggregate feedback:

SocialProof = f(likes, ratings, shares, reposts, comments, ranking, trend visibility)

A randomized design should distinguish true quality from manipulated popularity signals.

## Recommended reliability checks

- Normative pressure reliability
- Informational uncertainty reliability
- Group identification reliability
- Perceived unanimity reliability
- Status strength reliability
- Psychological safety reliability
- Dissent visibility reliability

## Recommended validity checks

- Confirm ambiguity manipulation increases perceived uncertainty.
- Confirm public-response manipulation increases visibility concerns.
- Confirm ally/dissent condition reduces perceived unanimity.
- Confirm status-strength manipulation increases perceived source credibility.
- Test whether visible dissent reduces conformity even when the majority remains numerically larger.
- Test whether digital popularity cues affect later ratings, judgments, or sharing.
