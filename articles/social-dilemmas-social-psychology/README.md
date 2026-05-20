# Social Dilemmas in Social Psychology

This folder contains reproducible research code for studying social dilemmas, public-goods games, commons dilemmas, free riding, conditional cooperation, reciprocity, trust, social norms, enforcement, institutional legitimacy, and collective-action failure.

The examples are designed for social psychologists, behavioral economists, political economists, environmental-governance researchers, commons scholars, organizational researchers, public-policy analysts, and computational social scientists.

## Research focus

The code operationalizes social dilemma research through:

- participant, group, and site identifiers
- experimental condition
- dilemma type
- round number
- endowment and contribution
- extraction from a common-pool resource
- public-goods multiplier or marginal per-capita return
- trust score
- norm salience
- enforcement signal
- fairness score
- institutional legitimacy
- monitoring strength
- sanction probability
- sanction severity
- reciprocity expectation
- resource stock
- group welfare
- free-riding index
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, contribution models, commons depletion models, punishment simulations, and institutional-design simulations
- `r/` — multilevel contribution models, commons extraction models, enforcement effects, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia` — commons and public-goods simulation
- `c` — fast contribution/free-riding simulator
- `cpp` — common-pool resource simulator
- `fortran` — repeated public-goods contribution model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/social_dilemmas_model.py --simulate --output data/social_dilemmas_trials.csv --outputs outputs
python3 python/social_dilemmas_model.py --input data/social_dilemmas_trials.csv --outputs outputs
Rscript r/social_dilemmas_analysis.R data/social_dilemmas_trials.csv outputs
go run go/validator.go data/social_dilemmas_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/social_dilemmas_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/social-dilemmas-social-psychology
