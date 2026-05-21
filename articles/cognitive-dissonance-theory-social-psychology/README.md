# Cognitive Dissonance Theory

This folder contains reproducible research code for studying cognitive dissonance, psychological inconsistency, forced compliance, post-decision spreading of alternatives, effort justification, belief disconfirmation, self-affirmation, self-concept threat, action-based conflict, institutional rationalization, and commitment escalation.

The examples are designed for social psychologists, cognitive psychologists, political psychologists, organizational researchers, behavioral scientists, communication researchers, decision scientists, and scholars studying belief persistence, moral rationalization, attitude change, ideology, and institutional inertia.

## Research focus

The code operationalizes cognitive dissonance research through:

- participant, session, group, scenario, site, and institutional identifiers
- experimental paradigm
- condition
- pre-attitude and post-attitude
- attitude change
- counter-attitudinal behavior
- perceived choice
- perceived responsibility
- identity threat
- self-affirmation
- justification availability
- public commitment
- effort cost
- outcome value
- chosen and rejected option values
- spreading of alternatives
- belief disconfirmation strength
- proselytizing intensity
- coherence pressure
- response latency
- institutional commitment
- sunk cost
- policy reversal willingness

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, dissonance models, decision-spreading models, institutional escalation simulation
- `r/` — multilevel attitude-change, commitment, effort-justification, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in WordPress
- `julia/` — institutional commitment-escalation simulation
- `c` — fast spreading-of-alternatives simulator
- `cpp` — policy-rationalization simulator
- `fortran` — coherence-pressure recurrence model
- `go` — CSV validation utility
- `rust` — fast paradigm-level summary utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/cognitive_dissonance_model.py --simulate --output data/dissonance_trials.csv --outputs outputs
python3 python/cognitive_dissonance_model.py --input data/dissonance_trials.csv --outputs outputs
Rscript r/cognitive_dissonance_analysis.R data/dissonance_trials.csv outputs
go run go/validator.go data/dissonance_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/dissonance_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/cognitive-dissonance-theory-social-psychology
