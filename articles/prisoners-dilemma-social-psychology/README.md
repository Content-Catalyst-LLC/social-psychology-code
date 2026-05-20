# Prisoner's Dilemma in Social Psychology

This folder contains reproducible research code for studying cooperation, defection, reciprocity, trust, fairness, repeated interaction, reputation, punishment, communication, institutional enforcement, and collective-action failures in prisoner’s dilemma settings.

The examples are designed for social psychologists, behavioral economists, game theorists, political psychologists, cooperation researchers, institutional analysts, computational social scientists, and researchers studying how trust and cooperation emerge or fail under strategic interdependence.

## Research focus

The code operationalizes prisoner’s dilemma research through:

- participant and dyad identifiers
- experimental condition
- round number
- own choice and partner choice
- cooperation and partner cooperation
- payoff parameters
- own payoff and partner payoff
- cumulative payoff
- trust score
- fairness score
- expected partner cooperation
- communication access
- punishment availability
- reputation visibility
- monitoring strength
- institutional enforcement
- social identity salience
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, cooperation models, repeated-game simulations, strategy tournaments, and institutional simulations
- `r/` — multilevel models, cooperation-rate estimates, reciprocity effects, payoff models, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — iterated prisoner’s dilemma strategy simulation
- `c` — fast repeated-game simulator
- `cpp` — strategy tournament simulator
- `fortran` — repeated cooperation model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/prisoners_dilemma_model.py --simulate --output data/prisoners_dilemma_trials.csv --outputs outputs
python3 python/prisoners_dilemma_model.py --input data/prisoners_dilemma_trials.csv --outputs outputs
Rscript r/prisoners_dilemma_analysis.R data/prisoners_dilemma_trials.csv outputs
go run go/validator.go data/prisoners_dilemma_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/prisoners_dilemma_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/prisoners-dilemma-social-psychology
