# Altruism in Social Psychology

This folder contains reproducible research code for studying altruism, empathy-induced helping, costly helping, recipient need, helping cost, kinship, reciprocity, moral identity, identity overlap, social norms, altruistic punishment, warm-glow giving, public-goods contribution, and institutional conditions that support other-regarding behavior.

The examples are designed for social psychologists, moral psychologists, behavioral economists, evolutionary theorists, cooperation researchers, nonprofit researchers, public-goods researchers, and institutional designers.

## Research focus

The code operationalizes altruism research through:

- participant, session, recipient, scenario, site, and group identifiers
- experimental condition
- empathy score
- personal distress
- helping cost
- recipient need
- recipient closeness
- identity overlap
- kinship coefficient
- reciprocity expectation
- reputation visibility
- moral identity
- social norm salience
- warm-glow expectation
- perceived efficacy
- intervention risk
- altruistic decision
- donation amount
- time volunteered
- altruistic punishment
- punishment cost
- public-goods contribution
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, empathy-altruism models, donation models, public-goods simulations, and altruistic-punishment simulations
- `r/` — multilevel altruistic-decision models, donation models, punishment models, and visualization
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — cooperation and altruistic-contribution simulation
- `c` — fast costly-helping simulator
- `cpp` — reciprocity and public-goods simulator
- `fortran` — Hamilton-rule / kin-selection utility
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/altruism_model.py --simulate --output data/altruism_trials.csv --outputs outputs
python3 python/altruism_model.py --input data/altruism_trials.csv --outputs outputs
Rscript r/altruism_analysis.R data/altruism_trials.csv outputs
go run go/validator.go data/altruism_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/altruism_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/altruism-social-psychology
