# Measurement Notes

## Authority-pressure index

AuthorityPressure = (
  authority_legitimacy
+ authority_proximity
+ institutional_prestige
+ command_clarity
+ cost_of_defiance
+ peer_compliance
- peer_dissent
) / 6

## Moral-resistance index

MoralResistance = (
  moral_conflict
+ victim_proximity
+ harm_salience
+ peer_dissent
+ perceived_responsibility_after
) / 5

## Identification index

Identification = (
  role_identification
+ mission_identification
+ institutional_prestige
) / 3

## Obedience probability

P(Obedience) = logit^-1(
  beta0
+ beta1*AuthorityLegitimacy
+ beta2*AuthorityProximity
+ beta3*InstitutionalPrestige
+ beta4*CostOfDefiance
+ beta5*EscalationStep
+ beta6*ResponsibilityDisplacement
+ beta7*RoleIdentification
+ beta8*MissionIdentification
- beta9*MoralConflict
- beta10*VictimProximity
- beta11*HarmSalience
- beta12*PeerDissent
)

## Resistance probability

P(Resistance) = logit^-1(
  gamma0
- gamma1*AuthorityPressure
+ gamma2*MoralResistance
+ gamma3*PeerDissent
+ gamma4*VictimProximity
+ gamma5*PerceivedResponsibility
- gamma6*CostOfDefiance
)

## Recommended reliability checks

- Authority legitimacy reliability
- Moral conflict reliability
- Responsibility displacement reliability
- Mission identification reliability
- Role identification reliability
- Resistance-support reliability

## Recommended validity checks

- Confirm legitimacy manipulation changed perceived authority legitimacy.
- Confirm peer-dissent condition increased perceived resistance support.
- Confirm harm-salience condition increased moral conflict.
- Confirm responsibility-displacement condition reduced perceived personal responsibility.
- Test whether mission identification predicts obedience beyond authority pressure.
- Test whether peer dissent reduces obedience across escalation steps.
