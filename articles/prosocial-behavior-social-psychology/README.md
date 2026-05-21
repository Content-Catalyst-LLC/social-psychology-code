# Prosocial Behavior in Social Psychology

This folder contains reproducible research code for studying prosocial behavior: helping, sharing, cooperation, volunteering, donation, emotional support, public-goods contribution, bystander intervention, organizational citizenship behavior, mutual aid, and institutional designs that support care and cooperation.

The examples are designed for social psychologists, behavioral economists, moral psychologists, organizational researchers, policy researchers, public-health researchers, nonprofit analysts, and public-goods scholars.

## Research focus

The code operationalizes prosocial behavior research through:

- participant, session, scenario, recipient, site, and group identifiers
- experimental condition
- context type
- empathy score
- perspective taking
- norm salience
- reciprocity expectation
- perceived efficacy
- helping cost
- intervention risk
- bystander count
- felt responsibility
- identity overlap
- group identification
- trust level
- moral identity
- reputation visibility
- institutional legitimacy
- helping decision
- donation amount
- volunteer minutes
- cooperation contribution
- emotional support
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, helping models, cooperation models, and public-goods simulations
- `r/` — multilevel helping, donation, cooperation, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — public-goods/prosocial contribution simulation
- `c` — fast helping-propensity simulator
- `cpp` — trust and cooperation simulator
- `fortran` — cumulative welfare contribution model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/prosocial_behavior_model.py --simulate --output data/prosocial_behavior_trials.csv --outputs outputs
python3 python/prosocial_behavior_model.py --input data/prosocial_behavior_trials.csv --outputs outputs
Rscript r/prosocial_behavior_analysis.R data/prosocial_behavior_trials.csv outputs
go run go/validator.go data/prosocial_behavior_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/prosocial_behavior_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/prosocial-behavior-social-psychology
