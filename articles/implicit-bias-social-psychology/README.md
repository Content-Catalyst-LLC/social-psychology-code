# Implicit Bias in Social Psychology

This folder contains reproducible research code for studying implicit bias, implicit social cognition, automatic associations, IAT-style response latency, explicit attitudes, behavioral outcomes, institutional decision processes, and bias-mitigation designs.

The examples are designed for social psychologists, cognitive psychologists, intergroup-relations researchers, healthcare-equity researchers, education researchers, organizational psychologists, public-policy researchers, and scholars studying discrimination, social cognition, and institutional fairness.

## Research focus

The code operationalizes implicit-bias research through:

- participant, session, group, scenario, site, and institution identifiers
- social category
- evaluative attribute
- congruent and incongruent task blocks
- trial-level response latency
- accuracy
- explicit attitude
- implicit-association score
- D-score computation
- cognitive load
- accountability
- time pressure
- counter-stereotypical exposure
- perspective-taking condition
- structured decision support
- institutional context
- judgment score
- behavioral outcome
- disparity contribution
- post-intervention follow-up

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic IAT-style data generation, D-score calculations, mixed/clustered models, intervention simulations
- `r/` — multilevel latency, judgment, D-score, and intervention models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in WordPress
- `julia/` — cumulative institutional disparity simulation
- `c` — fast latency-difference simulator
- `cpp` — institutional decision-threshold simulator
- `fortran` — cumulative disparity recurrence model
- `go` — CSV validation utility
- `rust` — fast D-score and summary utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/implicit_bias_model.py --simulate --output data/implicit_bias_trials.csv --outputs outputs
python3 python/implicit_bias_model.py --input data/implicit_bias_trials.csv --outputs outputs
Rscript r/implicit_bias_analysis.R data/implicit_bias_trials.csv outputs
go run go/validator.go data/implicit_bias_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/implicit_bias_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/implicit-bias-social-psychology
