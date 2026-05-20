# Measurement Notes

## Payoff structure

A canonical prisoner’s dilemma satisfies:

T > R > P > S

where:

- T = temptation payoff from unilateral defection
- R = reward payoff from mutual cooperation
- P = punishment payoff from mutual defection
- S = sucker’s payoff from unilateral cooperation against defection

A common additional condition is:

2R > T + S

which means mutual cooperation is collectively better than alternating exploitation.

## Cooperation model

P(Cooperate_i = 1) = logit^-1(beta0
    + beta1*Trust_i
    + beta2*ExpectedPartnerCooperation_i
    + beta3*Fairness_i
    + beta4*PartnerCooperation_{t-1}
    + beta5*Communication_i
    + beta6*ReputationVisibility_i
    + beta7*InstitutionalEnforcement_i
    - beta8*Temptation_i)

## Reciprocity

Reciprocity_i = P(C_i,t = 1 | PartnerC_i,t-1 = 1)
                - P(C_i,t = 1 | PartnerC_i,t-1 = 0)

## Exploitation sensitivity

DefectionAfterExploitation_i = P(D_i,t = 1 | PartnerD_i,t-1 = 1 and C_i,t-1 = 1)

## Repeated-game cooperation threshold

Cooperation is easier to sustain when:

delta >= (T - R) / (T - P)

where delta is the discount factor.

## Institutional enforcement

EffectiveTemptation_i = T_i - Sanction_i * DetectionProbability_i

Institutions stabilize cooperation when they reduce the expected net payoff from defection.

## Recommended reliability checks

- Trust scale reliability
- Fairness scale reliability
- Expectation scale reliability
- Strategy classification reliability
- Response-time filtering rules
- Incentive comprehension checks

## Recommended validity checks

- Verify payoff-matrix comprehension.
- Confirm the payoff structure matches prisoner’s dilemma inequalities.
- Test whether partner cooperation in previous rounds predicts own cooperation.
- Test whether communication increases cooperation through expectations or trust.
- Test whether sanctions alter the expected payoff of defection.
- Test whether cooperation differs under finite versus uncertain horizon.
