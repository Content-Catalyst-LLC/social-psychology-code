# Measurement Notes

## Global moral-disengagement index

MD_i = w1*MJ_i + w2*EL_i + w3*AC_i + w4*DR_i
     + w5*DF_i + w6*DC_i + w7*DH_i + w8*VB_i

Where:

- MJ = moral justification
- EL = euphemistic labeling
- AC = advantageous comparison
- DR = displacement of responsibility
- DF = diffusion of responsibility
- DC = distortion of consequences
- DH = dehumanization
- VB = victim blame or attribution of blame

## Moral self-sanction inhibition

SelfSanction_i = MoralStandard_i - MD_i + HarmVisibility_i + ResponsibilityClarity_i

## Harmful-decision propensity

P(Harm_i = 1) = logit^-1(beta0 + beta1*MD_i - beta2*Empathy_i
                         - beta3*Guilt_i - beta4*ResponsibilityClarity_i
                         + beta5*InstitutionalPressure_i)

## Responsibility displacement

PerceivedAgency_i = BaselineAgency_i - gamma1*AuthorityPressure_i
                    - gamma2*ResponsibilityDisplacement_i
                    - gamma3*ResponsibilityDiffusion_i

## Consequence distortion

PerceivedHarm_i = ActualHarm_i - delta1*ConsequenceDistortion_i
                  - delta2*VictimDistance_i + delta3*HarmVisibility_i

## Normalization over time

NormHarm_{t+1} = NormHarm_t + eta1*MeanMD_t + eta2*RewardForHarm_t
                - eta3*Accountability_t - eta4*DissentProtection_t

## Recommended reliability checks

- Mechanism-specific item reliability
- Global moral-disengagement index reliability
- Measurement invariance across groups or contexts
- Harmful-decision task reliability
- Response-time filtering rules

## Recommended validity checks

- Compare mechanism-specific effects with global index effects
- Distinguish state mechanisms from trait propensity
- Test whether harm visibility reduces harmful choices
- Test whether responsibility clarity reduces displacement/diffusion effects
- Test whether dissent protection interrupts normalization
- Test whether mechanism effects are mediated by empathy or guilt
- Test whether authority pressure moderates displacement of responsibility
