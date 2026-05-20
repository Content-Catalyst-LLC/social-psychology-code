# The Contact Hypothesis and Intergroup Contact

This folder contains reproducible research code for studying the contact hypothesis, intergroup contact, prejudice reduction, intergroup anxiety, empathy, trust, institutional support, equal-status contact, common goals, cooperation, indirect contact, negative contact, and longitudinal attitude change.

The examples support work in social psychology, political psychology, prejudice reduction, education, workplace diversity research, intergroup dialogue, conflict transformation, community studies, and mixed-methods social science.

## Research focus

The code operationalizes intergroup contact through:

- participant and site identifiers
- group membership and target group
- experimental or observational condition
- contact frequency
- contact quality
- equal status
- common goals
- cooperation
- institutional support
- voluntariness
- negative contact
- indirect contact
- extended contact
- intergroup anxiety
- empathy
- perspective taking
- trust
- perceived threat
- prejudice score
- stereotype endorsement
- willingness for future contact
- social distance
- inclusive norm perception
- response time
- longitudinal wave

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, mixed models, mediation-style summaries, and contact-diffusion simulation
- `r/` — multilevel analysis, mediation-oriented summaries, longitudinal models, and visualizations
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — longitudinal contact-attitude simulation
- `c` — fast contact-prejudice simulator
- `cpp` — network-based contact diffusion simulator
- `fortran` — repeated-contact attitude-change simulator
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/contact_hypothesis_model.py --simulate --output data/contact_hypothesis_trials.csv --outputs outputs
python3 python/contact_hypothesis_model.py --input data/contact_hypothesis_trials.csv --outputs outputs
Rscript r/contact_hypothesis_analysis.R data/contact_hypothesis_trials.csv outputs
go run go/validator.go data/contact_hypothesis_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/contact_hypothesis_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/contact-hypothesis-intergroup-contact-reduces-prejudice
