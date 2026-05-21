# Measurement Notes

## IAT-style latency difference

D = (MeanRT_incongruent - MeanRT_congruent) / PooledSD

## Trial-level latency model

log(RT_ijt) = beta0
  + beta1*IncongruentBlock_ijt
  + beta2*ExplicitAttitude_i
  + beta3*CognitiveLoad_ijt
  + beta4*TimePressure_ijt
  - beta5*Accountability_ijt
  + u_i + v_j + error_ijt

## Judgment model

Judgment = alpha0
  + alpha1*DScore
  + alpha2*ExplicitAttitude
  + alpha3*TimePressure
  + alpha4*CognitiveLoad
  - alpha5*StructuredDecisionSupport
  + error

## Institutional accumulation

Disparity_total = sum(decision_bias_t)

Small asymmetries can become consequential when repeated across hiring, evaluation, healthcare, discipline, promotion, or resource-allocation decisions.

## Recommended reliability checks

- Split-half reliability for implicit measure
- Internal consistency for explicit attitude scale
- Reliability of judgment ratings
- Test-retest stability where relevant
- Inter-rater reliability for coded decisions

## Recommended validity checks

- Compare implicit and explicit measures.
- Test whether implicit scores predict judgment beyond explicit attitude.
- Test whether effects grow under time pressure or cognitive load.
- Test whether accountability or structured decision support reduces outcome disparity.
- Test whether intervention effects persist after delay.
