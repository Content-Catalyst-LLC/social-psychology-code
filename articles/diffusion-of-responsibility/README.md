# Diffusion of Responsibility in Social Psychology

This folder contains reproducible research code for studying diffusion of responsibility, bystander intervention, pluralistic ignorance, evaluation apprehension, role clarity, emergency response, organizational accountability, and collective inaction.

The examples are designed for social psychologists, helping-behavior researchers, organizational psychologists, emergency-response researchers, institutional-accountability researchers, public-safety analysts, and computational social scientists studying how responsibility becomes diluted across groups.

## Research focus

The code operationalizes diffusion of responsibility through:

- participant and site identifiers
- experimental condition
- bystander count
- group size
- ambiguity level
- private concern
- perceived group concern
- pluralistic ignorance gap
- evaluation apprehension
- perceived personal responsibility
- role clarity
- intervention efficacy
- social visibility
- leadership cue
- accountability assignment
- organizational fragmentation
- intervention decision
- reporting decision
- intervention delay
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, intervention models, organizational-fragmentation models, and collective-inaction simulations
- `r/` — multilevel models, intervention-rate estimates, group-size moderation, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — organizational accountability-fragmentation simulation
- `c` — fast responsibility-diffusion simulator
- `cpp` — emergency response simulation by group size and clarity
- `fortran` — repeated intervention-propensity model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/diffusion_responsibility_model.py --simulate --output data/diffusion_responsibility_trials.csv --outputs outputs
python3 python/diffusion_responsibility_model.py --input data/diffusion_responsibility_trials.csv --outputs outputs
Rscript r/diffusion_responsibility_analysis.R data/diffusion_responsibility_trials.csv outputs
go run go/validator.go data/diffusion_responsibility_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/diffusion_responsibility_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/diffusion-of-responsibility
