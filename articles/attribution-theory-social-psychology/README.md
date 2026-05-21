# Attribution Theory

This folder contains reproducible research code for studying attribution theory, causal explanation, dispositional attribution, situational attribution, covariation reasoning, correspondent inference, attribution bias, responsibility judgment, achievement attribution, hostile attribution bias, actor-observer asymmetry, culture and agency, and institutional blame.

The examples are designed for social psychologists, cognitive psychologists, education researchers, organizational researchers, legal scholars, conflict researchers, communication scholars, public-policy researchers, and scholars studying responsibility, blame, motivation, and social inference.

## Research focus

The code operationalizes attribution research through:

- participant, session, group, scenario, site, and institutional identifiers
- target type and actor-observer perspective
- behavior domain
- outcome valence
- ambiguity level
- intentionality
- perceived choice
- perceived effort
- perceived ability
- situational constraint
- consensus
- distinctiveness
- consistency
- internal attribution
- external attribution
- stability
- controllability
- responsibility rating
- blame rating
- sympathy rating
- anger rating
- punishment support
- help support
- achievement expectation
- hostile attribution score
- attributional complexity
- cultural agency orientation
- response latency

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, attribution models, responsibility models, covariation models, institutional blame simulation
- `r/` — multilevel attribution, responsibility, hostile-attribution, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in WordPress
- `julia/` — institutional blame and correction simulation
- `c` — fast covariation attribution simulator
- `cpp` — responsibility-judgment simulator
- `fortran` — attribution-expectation recurrence model
- `go` — CSV validation utility
- `rust` — fast attribution-level summary utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/attribution_theory_model.py --simulate --output data/attribution_trials.csv --outputs outputs
python3 python/attribution_theory_model.py --input data/attribution_trials.csv --outputs outputs
Rscript r/attribution_theory_analysis.R data/attribution_trials.csv outputs
go run go/validator.go data/attribution_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/attribution_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/attribution-theory-social-psychology
