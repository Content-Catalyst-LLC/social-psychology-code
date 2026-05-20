# Social Comparison Theory in Social Psychology

This folder contains reproducible research code for studying social comparison theory, upward comparison, downward comparison, lateral comparison, attainability, identity relevance, self-evaluation, motivation, envy, inspiration, relative deprivation, digital comparison, organizational comparison, social norms, and institutional benchmarking.

The examples are designed for social psychologists, organizational researchers, digital media researchers, behavioral scientists, well-being researchers, and computational social scientists studying how people evaluate themselves through reference groups and social standards.

## Research focus

The code operationalizes social comparison through:

- participant and site identifiers
- experimental condition
- comparison type
- comparison direction
- comparison target status
- comparison domain
- reference group
- attainability
- similarity
- identity relevance
- perceived gap
- self-evaluation before and after comparison
- motivation
- affect
- envy
- inspiration
- self-esteem
- perceived fairness
- relative deprivation
- norm perception
- digital exposure
- organizational benchmarking
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, self-evaluation models, motivation models, digital comparison models, and benchmarking simulations
- `r/` — multilevel models, interaction effects, condition summaries, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — longitudinal comparison dynamics simulation
- `c` — fast comparison-gap simulator
- `cpp` — organizational benchmarking simulator
- `fortran` — repeated comparison affect simulation
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/social_comparison_model.py --simulate --output data/social_comparison_trials.csv --outputs outputs
python3 python/social_comparison_model.py --input data/social_comparison_trials.csv --outputs outputs
Rscript r/social_comparison_analysis.R data/social_comparison_trials.csv outputs
go run go/validator.go data/social_comparison_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/social_comparison_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/social-comparison-theory-social-psychology
