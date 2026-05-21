# Groupthink in Social Psychology

This folder contains reproducible research code for studying groupthink: cohesion, directive leadership, insulation, stress, consensus pressure, self-censorship, mindguarding, illusion of unanimity, dissent visibility, outside information, alternative search, risk analysis, contingency planning, decision quality, and institutional safeguards.

The examples are designed for social psychologists, organizational researchers, political psychologists, public-policy researchers, governance scholars, leadership researchers, crisis decision researchers, collective-intelligence researchers, and decision scientists.

## Research focus

The code operationalizes groupthink research through:

- participant, group, session, scenario, site, and institution identifiers
- cohesion
- leadership directiveness
- group insulation
- stress level
- consensus pressure
- self-censorship
- illusion of invulnerability
- illusion of unanimity
- belief in inherent morality
- outgroup stereotyping
- direct pressure on dissenters
- mindguarding
- dissent visibility
- outside information
- alternative search breadth
- risk analysis quality
- contingency planning
- devil’s advocate presence
- independent expert consultation
- subgroup review
- leader impartiality
- psychological safety
- decision quality
- forecast calibration
- implementation risk
- post-decision review quality
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, groupthink-risk models, decision-quality models, and safeguard simulations
- `r/` — multilevel decision-quality, self-censorship, consensus-pressure, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — crisis decision and safeguard simulation
- `c` — fast groupthink-risk index simulator
- `cpp` — institutional safeguard simulator
- `fortran` — repeated consensus-pressure recurrence model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/groupthink_model.py --simulate --output data/groupthink_trials.csv --outputs outputs
python3 python/groupthink_model.py --input data/groupthink_trials.csv --outputs outputs
Rscript r/groupthink_analysis.R data/groupthink_trials.csv outputs
go run go/validator.go data/groupthink_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/groupthink_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/groupthink-in-social-psychology
