# Self-Serving Bias in Social Psychology

This folder contains reproducible research code for studying self-serving attributional bias, success/failure attribution, self-enhancement, self-protection, responsibility judgment, blame deflection, accountability, leadership narratives, team attribution conflict, cultural variation, and institutional learning.

The examples are designed for social psychologists, attribution researchers, organizational psychologists, behavioral scientists, leadership researchers, political psychologists, and computational social scientists studying how people explain success and failure.

## Research focus

The code operationalizes self-serving bias through:

- participant and site identifiers
- experimental condition
- outcome valence
- actor target: self, other, team, leader, institution, or outgroup
- internal attribution
- external attribution
- stable attribution
- controllable attribution
- responsibility rating
- blame rating
- credit claiming
- excuse making
- self-esteem
- ego threat
- task importance
- outcome expectancy
- perceived fairness
- evidence strength
- learning intention
- accountability pressure
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, attribution asymmetry models, accountability models, and organizational learning simulations
- `r/` — multilevel models, self-serving bias scores, moderation analysis, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — repeated performance-attribution simulation
- `c` — fast attribution asymmetry simulator
- `cpp` — organizational credit/blame simulator
- `fortran` — repeated outcome attribution model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/self_serving_bias_model.py --simulate --output data/self_serving_bias_trials.csv --outputs outputs
python3 python/self_serving_bias_model.py --input data/self_serving_bias_trials.csv --outputs outputs
Rscript r/self_serving_bias_analysis.R data/self_serving_bias_trials.csv outputs
go run go/validator.go data/self_serving_bias_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/self_serving_bias_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/self-serving-bias-social-psychology
