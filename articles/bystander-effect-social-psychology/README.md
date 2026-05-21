# The Bystander Effect in Social Psychology

This folder contains reproducible research code for studying the bystander effect, bystander intervention, diffusion of responsibility, pluralistic ignorance, evaluation apprehension, emergency clarity, victim identifiability, shared identity, direct responsibility assignment, online bystander behavior, cyberbullying intervention, and institutional response design.

The examples are designed for social psychologists, applied psychologists, emergency-response researchers, education researchers, organizational scholars, cyberbullying researchers, platform-governance researchers, and public-safety practitioners.

## Research focus

The code operationalizes bystander-effect research through:

- participant, session, scenario, site, and group identifiers
- bystander count
- perceived bystander count
- emergency clarity
- danger level
- victim identifiability
- shared identity
- diffusion of responsibility
- pluralistic ignorance
- evaluation apprehension
- perceived competence
- perceived cost of intervention
- direct responsibility assignment
- leadership cue
- intervention norm salience
- intervention type
- intervention likelihood
- actual intervention
- intervention latency
- online context and platform traceability
- moderation visibility
- response confidence

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, intervention models, latency models, bystander simulations, and online intervention simulations
- `r/` — multilevel intervention models, logistic models, latency models, and visualization
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — diffusion-of-responsibility and threshold simulation
- `c` — fast helping-probability simulator
- `cpp` — direct-responsibility assignment simulator
- `fortran` — intervention-threshold model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/bystander_effect_model.py --simulate --output data/bystander_effect_trials.csv --outputs outputs
python3 python/bystander_effect_model.py --input data/bystander_effect_trials.csv --outputs outputs
Rscript r/bystander_effect_analysis.R data/bystander_effect_trials.csv outputs
go run go/validator.go data/bystander_effect_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/bystander_effect_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/bystander-effect-social-psychology
