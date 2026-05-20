# Collective Action and Social Change

This folder contains reproducible research code for studying collective action, protest participation, mobilization, social identity, perceived injustice, moral outrage, collective efficacy, network support, participation costs, free-riding, digital mobilization, and institutional response.

The examples are designed for social psychologists, political psychologists, social movement researchers, civic data analysts, behavioral scientists, and computational social scientists studying how private grievance becomes coordinated public action.

## Research focus

The code operationalizes collective action through:

- participant and group identifiers
- experimental or observational condition
- social identity strength
- perceived injustice
- moral outrage
- collective efficacy
- network support
- mobilization exposure
- participation cost
- perceived repression risk
- free-rider incentive
- participation intention
- actual participation
- action type
- digital engagement
- offline engagement
- recruitment source
- institutional response
- perceived legitimacy
- movement outcome
- response time
- network edges
- event logs

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, participation models, mobilization simulations, and network analysis
- `r/` — mixed-effects, logistic, mediation-style, and summary workflows
- `sql/` — relational schema, views, and reproducible research queries
- `julia/` — threshold and diffusion simulation for mobilization dynamics
- `c/` — fast participation-threshold simulator
- `cpp/` — network cascade and recruitment simulator
- `fortran/` — efficacy and participation propensity model
- `go/` — CSV validation utility
- `rust/` — fast summary and data-quality utility
- `notebooks/` — notebook workflow scaffold
- `docs/` — methodological protocol and measurement notes
- `outputs/` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/collective_action_model.py --simulate --output data/collective_action_trials.csv --outputs outputs
python3 python/collective_action_model.py --input data/collective_action_trials.csv --outputs outputs
Rscript r/collective_action_analysis.R data/collective_action_trials.csv outputs
go run go/validator.go data/collective_action_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/collective_action_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/collective-action-and-social-change
