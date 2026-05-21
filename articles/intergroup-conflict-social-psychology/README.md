# Intergroup Conflict in Social Psychology

This folder contains reproducible research code for studying intergroup conflict: realistic conflict, resource competition, social identity, status threat, symbolic threat, stereotypes, perceived injustice, polarization, intergroup anxiety, contact, superordinate goals, cooperative tasks, institutional legitimacy, escalation dynamics, and conflict-reduction interventions.

The examples are designed for social psychologists, political psychologists, conflict researchers, organizational researchers, public-policy researchers, peace and reconciliation scholars, and researchers studying collective behavior, identity, prejudice, and cooperation.

## Research focus

The code operationalizes intergroup conflict research through:

- participant, group, session, scenario, site, and dyad identifiers
- in-group and out-group labels
- resource competition
- zero-sum perception
- identity salience
- group identification
- status threat
- symbolic threat
- realistic threat
- stereotype endorsement
- outgroup warmth
- outgroup competence
- intergroup anxiety
- perceived injustice
- dehumanization
- perceived legitimacy
- institutional trust
- norm of retaliation
- group polarization
- hostility score
- aggression intention
- avoidance intention
- support for exclusion
- support for cooperation
- contact quality
- equal status
- common goal salience
- institutional support
- cooperative task success
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, hostility models, contact models, escalation simulations, and intervention simulations
- `r/` — multilevel hostility, aggression, exclusion, cooperation, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — escalation and superordinate-goal simulation
- `c` — fast conflict-intensity simulator
- `cpp` — contact/intervention simulator
- `fortran` — escalation recurrence model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/intergroup_conflict_model.py --simulate --output data/intergroup_conflict_trials.csv --outputs outputs
python3 python/intergroup_conflict_model.py --input data/intergroup_conflict_trials.csv --outputs outputs
Rscript r/intergroup_conflict_analysis.R data/intergroup_conflict_trials.csv outputs
go run go/validator.go data/intergroup_conflict_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/intergroup_conflict_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/intergroup-conflict-social-psychology
