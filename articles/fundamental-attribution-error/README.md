# Fundamental Attribution Error

This folder contains reproducible research code for studying the fundamental attribution error, correspondence bias, dispositional inference, situational constraint neglect, actor-observer asymmetry, cognitive load, cultural variation, institutional judgment, and accountability in attribution.

The examples are designed for social psychologists, attribution researchers, organizational psychologists, legal and policy researchers, cultural psychologists, and computational social scientists studying how observers infer character, intention, or disposition from behavior.

## Research focus

The code operationalizes attributional judgment through:

- participant and site identifiers
- experimental condition
- actor role and observer role
- behavior valence
- dispositional attribution
- situational attribution
- perceived constraint
- choice freedom
- cognitive load
- perspective-taking condition
- accountability pressure
- evidence strength
- correspondence inference
- moral blame
- punishment recommendation
- empathy
- cultural orientation
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, attribution models, bias scores, and institutional simulation
- `r/` — multilevel models, condition summaries, interaction effects, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — longitudinal attribution-correction simulation
- `c` — fast dispositional-inference simulator
- `cpp` — institutional blame/punishment simulator
- `fortran` — situational-constraint neglect simulator
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/fundamental_attribution_error_model.py --simulate --output data/fundamental_attribution_error_trials.csv --outputs outputs
python3 python/fundamental_attribution_error_model.py --input data/fundamental_attribution_error_trials.csv --outputs outputs
Rscript r/fundamental_attribution_error_analysis.R data/fundamental_attribution_error_trials.csv outputs
go run go/validator.go data/fundamental_attribution_error_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/fundamental_attribution_error_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/fundamental-attribution-error
