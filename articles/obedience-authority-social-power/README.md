# Obedience, Authority, and Social Power

This folder contains reproducible research code for studying obedience, authority, hierarchy, compliance, legitimacy, responsibility displacement, moral conflict, peer dissent, resistance, and institutional safeguards.

The examples are designed for social psychologists, political psychologists, organizational researchers, institutional sociologists, governance scholars, legal scholars, ethics researchers, public-policy researchers, and researchers studying authority, hierarchy, moral agency, and social power.

## Research focus

The code operationalizes obedience research through:

- participant, session, group, scenario, site, and institutional identifiers
- authority legitimacy
- authority proximity
- institutional prestige
- command clarity
- cost of defiance
- escalation step
- responsibility displacement
- moral conflict
- victim proximity
- harm salience
- peer dissent
- peer compliance
- role identification
- mission identification
- obedience outcome
- resistance outcome
- hesitation
- protest
- response time
- perceived responsibility after action
- institutional safeguard conditions
- resistance-support conditions

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, obedience models, escalation models, and resistance simulations
- `r/` — multilevel obedience, resistance, response-time, and escalation models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in WordPress
- `julia/` — escalation and dissent simulation
- `c` — fast authority-pressure simulator
- `cpp` — institutional-safeguard simulator
- `fortran` — incremental escalation recurrence model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/obedience_authority_model.py --simulate --output data/obedience_trials.csv --outputs outputs
python3 python/obedience_authority_model.py --input data/obedience_trials.csv --outputs outputs
Rscript r/obedience_authority_analysis.R data/obedience_trials.csv outputs
go run go/validator.go data/obedience_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/obedience_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/obedience-authority-social-power
