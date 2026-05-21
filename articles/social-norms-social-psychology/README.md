# Social Norms in Social Psychology

This folder contains reproducible research code for studying social norms: descriptive norms, injunctive norms, empirical expectations, normative expectations, sanctions, norm salience, reference groups, pluralistic ignorance, conditional preference, norm misperception, institutional legitimacy, policy-message design, norm tipping, and norm change.

The examples are designed for social psychologists, behavioral economists, institutional researchers, public-policy researchers, public-health researchers, organizational scholars, development practitioners, and researchers studying collective behavior and social change.

## Research focus

The code operationalizes social-norms research through:

- participant, session, scenario, site, reference group, and policy domain identifiers
- descriptive norm perception
- injunctive norm perception
- empirical expectations
- normative expectations
- personal attitude
- norm salience
- sanction salience
- sanction severity
- reward salience
- reference-group identification
- perceived legitimacy
- trust in institution
- pluralistic ignorance
- perceived trend / dynamic norm
- message type
- compliance decision
- compliance intention
- contribution amount
- reporting behavior
- response time
- norm threshold
- tipping exposure
- post-message norm perception

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, norm-compliance models, message experiments, threshold dynamics, and policy simulations
- `r/` — multilevel norm-compliance, reaction-time, contribution, and message-effect models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — threshold and tipping simulations
- `c` — fast norm-threshold simulator
- `cpp` — descriptive/injunctive message simulator
- `fortran` — norm-equilibrium and tipping model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/social_norms_model.py --simulate --output data/social_norms_trials.csv --outputs outputs
python3 python/social_norms_model.py --input data/social_norms_trials.csv --outputs outputs
Rscript r/social_norms_analysis.R data/social_norms_trials.csv outputs
go run go/validator.go data/social_norms_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/social_norms_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/social-norms-social-psychology
