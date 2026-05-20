# Measurement Notes

## SIMCA-style participation model

Pr(action) = logistic(beta0 + beta1 * identity + beta2 * injustice + beta3 * efficacy + beta4 * network_support - beta5 * participation_cost)

## Moral outrage pathway

moral_outrage = alpha0 + alpha1 * perceived_injustice + alpha2 * identity_strength + error

## Collective efficacy update

E_{t+1} = E_t + mu * visible_mobilization_t - rho * repression_t

## Free-rider pressure

free_rider_pressure = public_benefit / group_size - private_cost

## Network exposure

network_exposure_i = sum_j A_ij * participation_j

where A_ij is an adjacency relation from participant i to participant j.

## Threshold participation

participant i joins if:

identity_i + injustice_i + efficacy_i + network_exposure_i - cost_i >= threshold_i

## Event-level mobilization

mobilization_rate = participants / eligible_population

## Institutional response coding

Suggested categories:

- no_response
- symbolic_response
- negotiation
- concession
- reform
- repression
- cooptation
- escalation
- backlash

## Digital/offline distinction

Digital engagement and offline participation should be stored separately. A petition signature, a post share, a protest attendance record, a donation, and organizing labor are different forms of action with different costs and consequences.

## Recommended reliability checks

- Scale reliability for identity, injustice, outrage, efficacy, legitimacy, and support
- Split-half reliability for multi-item measures
- Test-retest reliability in panel studies
- Intercoder reliability for event and institutional-response coding
- Network-data missingness diagnostics

## Recommended validity checks

- Convergent validity with protest intention, petition signing, donation, attendance, and organizing labor
- Discriminant validity between personal grievance and group-based injustice
- Measurement invariance across groups where appropriate
- Sensitivity analysis for repression risk and participation cost
- Network clustering and dependence diagnostics
