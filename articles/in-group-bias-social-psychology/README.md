# In-Group Bias in Social Psychology

This folder contains reproducible research code for studying in-group bias, intergroup favoritism, trust asymmetry, moral judgment asymmetry, resource allocation, social identity salience, perceived threat, group norms, minimal-group effects, institutional favoritism, and fairness outcomes.

The examples are designed for social psychologists, political psychologists, organizational researchers, behavioral economists, institutional analysts, and computational social scientists studying how group membership shapes trust, evaluation, allocation, and moral judgment.

## Research focus

The code operationalizes in-group bias through:

- participant and site identifiers
- experimental or observational condition
- target group relation
- in-group target indicator
- identity salience
- group identification
- perceived threat
- norm strength
- status asymmetry
- trust rating
- fairness rating
- competence rating
- warmth rating
- empathy rating
- moral blame
- moral forgiveness
- punishment severity
- reward allocation
- resource allocation
- cooperation choice
- response time
- institutional decision context

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, trust/allocation models, moral asymmetry models, and network simulation
- `r/` — multilevel models, interaction terms, condition summaries, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — repeated in-group/out-group allocation simulation
- `c` — fast bias-differential simulator
- `cpp` — minimal-group allocation simulator
- `fortran` — identity-salience favoritism simulator
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/ingroup_bias_model.py --simulate --output data/ingroup_bias_trials.csv --outputs outputs
python3 python/ingroup_bias_model.py --input data/ingroup_bias_trials.csv --outputs outputs
Rscript r/ingroup_bias_analysis.R data/ingroup_bias_trials.csv outputs
go run go/validator.go data/ingroup_bias_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/ingroup_bias_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/in-group-bias-social-psychology
