# Stereotypes, Prejudice, and Discrimination

This folder contains reproducible research code for studying stereotypes, prejudice, discrimination, social categorization, stereotype content, perceived threat, intergroup contact, stereotype threat, implicit-explicit associations, discriminatory decision tendencies, and cumulative institutional inequality.

The examples are designed for social psychologists, intergroup-relations researchers, sociologists, organizational researchers, education researchers, public-policy researchers, legal scholars, health-equity researchers, and scholars studying bias, exclusion, social hierarchy, and institutional inequality.

## Research focus

The code operationalizes stereotypes and prejudice research through:

- participant, session, group, scenario, site, and institutional identifiers
- target group
- evaluator group
- stereotype strength
- warmth and competence ratings
- prejudice rating
- perceived threat
- perceived competition
- perceived status
- social distance
- intergroup contact quality
- institutional support
- stereotype threat salience
- identity salience
- implicit association score
- explicit attitude score
- discrimination tendency
- behavioral outcome
- response latency
- decision stage
- cumulative disparity

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, prejudice models, contact models, stereotype-threat models, institutional-disparity simulations
- `r/` — multilevel prejudice, discrimination, stereotype-content, response-time, and intervention models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in WordPress
- `julia/` — cumulative inequality and contact-intervention simulation
- `c` — fast illusory-correlation simulator
- `cpp` — institutional disparity simulator
- `fortran` — cumulative-disparity recurrence model
- `go` — CSV validation utility
- `rust` — fast group-level summary utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/stereotypes_prejudice_model.py --simulate --output data/stereotypes_prejudice_trials.csv --outputs outputs
python3 python/stereotypes_prejudice_model.py --input data/stereotypes_prejudice_trials.csv --outputs outputs
Rscript r/stereotypes_prejudice_analysis.R data/stereotypes_prejudice_trials.csv outputs
go run go/validator.go data/stereotypes_prejudice_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/stereotypes_prejudice_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/stereotypes-prejudice-social-psychology
