# Tragedy of the Commons in Social Psychology

This folder contains reproducible research code for studying commons dilemmas, common-pool resources, open-access failure, governed commons, extraction behavior, resource depletion, cooperation, monitoring, sanctions, institutional legitimacy, fairness, stewardship, and polycentric governance.

The examples are designed for social psychologists, environmental-governance researchers, commons scholars, behavioral economists, political economists, sustainability researchers, public-policy analysts, and computational social scientists.

## Research focus

The code operationalizes tragedy-of-the-commons research through:

- participant, group, community, and site identifiers
- governance condition
- property regime
- round or period
- extraction level
- sustainable extraction threshold
- resource stock and regeneration
- trust score
- legitimacy score
- monitoring credibility
- sanction probability and severity
- boundary clarity
- rule participation
- conflict-resolution access
- local ecological knowledge
- perceived fairness
- reciprocity expectation
- stewardship norm salience
- inequality/asymmetry
- institutional effectiveness
- depletion risk
- group welfare
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, extraction models, depletion simulations, institutional-effectiveness models, and polycentric governance simulations
- `r/` — multilevel extraction models, resource-stock models, governance-condition estimates, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia` — commons resource depletion and governance simulation
- `c` — fast open-access depletion simulator
- `cpp` — common-pool resource governance simulator
- `fortran` — repeated extraction and regeneration model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/tragedy_commons_model.py --simulate --output data/tragedy_commons_trials.csv --outputs outputs
python3 python/tragedy_commons_model.py --input data/tragedy_commons_trials.csv --outputs outputs
Rscript r/tragedy_commons_analysis.R data/tragedy_commons_trials.csv outputs
go run go/validator.go data/tragedy_commons_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/tragedy_commons_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/tragedy-of-the-commons-social-psychology
