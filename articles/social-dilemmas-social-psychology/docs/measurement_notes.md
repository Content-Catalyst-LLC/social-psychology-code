# Measurement Notes

## Public-goods payoff

u_i = y_i - c_i + alpha * sum(c_j)

where:

- y_i = individual endowment
- c_i = individual contribution
- alpha = marginal per-capita return from the public good

A public-goods dilemma typically requires:

0 < alpha < 1 and n * alpha > 1

Individual contribution is privately costly, but total group contribution is collectively beneficial.

## Commons extraction

X_t = sum(x_i,t)

R_{t+1} = R_t + g(R_t) - X_t

where:

- X_t = total extraction
- R_t = resource stock
- g(R_t) = regeneration function

A commons dilemma occurs when individually rational extraction exceeds regenerative capacity.

## Free-riding index

FreeRide_i = (Endowment_i - Contribution_i) / Endowment_i

For public-goods contexts, this captures retained private benefit.

## Cooperation probability

P(Cooperate_i = 1) = logit^-1(beta0
    + beta1*Trust_i
    + beta2*NormSalience_i
    + beta3*EnforcementSignal_i
    + beta4*InstitutionalLegitimacy_i
    + beta5*ReciprocityExpectation_i
    - beta6*Temptation_i)

## Institutional effectiveness

InstitutionalEffect_i = MonitoringStrength_i * SanctionProbability_i * SanctionSeverity_i * Legitimacy_i

Sanctions without legitimacy can backfire; legitimacy without monitoring may be insufficient.

## Recommended reliability checks

- Trust scale reliability
- Norm salience scale reliability
- Institutional legitimacy scale reliability
- Fairness scale reliability
- Comprehension checks for payoff rules
- Response-time filtering rules

## Recommended validity checks

- Confirm MPCR conditions in public-goods games.
- Confirm depletion/regeneration assumptions in commons games.
- Test whether communication increases expectations and contributions.
- Test whether enforcement raises cooperation through credibility and legitimacy.
- Test whether punishment without legitimacy reduces trust.
- Test whether asymmetry predicts fairness judgments and cooperation decline.
