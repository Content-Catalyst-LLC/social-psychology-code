# Social Loafing in Social Psychology

This folder contains reproducible research assets for studying social loafing, the Ringelmann effect, motivation loss in groups, identifiability, accountability, task value, task uniqueness, perceived instrumentality, free-riding expectations, sucker-effect concerns, social compensation, distributed teamwork, and digital traceability.

## Research questions

- Does individual effort decline as group size increases?
- Does identifiability reduce social loafing?
- Does accountability reduce motivation loss?
- Does task value or task uniqueness increase collective effort?
- Does perceived instrumentality mediate the relationship between accountability and effort?
- Do distributed teams show greater loafing when digital traceability is low?
- Can version history, task logs, peer review, or dashboards reduce effort loss?
- When does social compensation offset social loafing?

## Folder structure

- `data/` — sample data and data dictionary
- `python/` — synthetic-data generation, models, and collective-effort simulations
- `r/` — multilevel models, summary tables, and plots
- `sql/` — database schema and analytical queries
- `julia/` — group-size and collective-effort simulation
- `c`, `cpp`, `fortran` — lightweight performance simulators
- `go`, `rust` — validation and fast summaries
- `docs/` — research protocol and measurement notes
- `notebooks/` — notebook scaffold
- `outputs/` — generated results

## Example commands

```bash
python3 python/social_loafing_model.py --simulate --output data/social_loafing_trials.csv --outputs outputs
python3 python/social_loafing_model.py --input data/social_loafing_trials.csv --outputs outputs
Rscript r/social_loafing_analysis.R data/social_loafing_trials.csv outputs
go run go/validator.go data/social_loafing_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/social_loafing_trials.csv
make all
```

Repository URL:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/social-loafing-social-psychology
