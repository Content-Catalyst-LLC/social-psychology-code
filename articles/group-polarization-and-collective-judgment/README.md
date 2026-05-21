# Group Polarization and Collective Judgment

This folder contains reproducible research code for studying group polarization and collective judgment: pre-post attitude shifts, risky and cautious shifts, persuasive-argument exposure, social comparison, identity salience, norm enforcement, informational homogeneity, dissent quality, confidence amplification, deliberation structure, algorithmic reinforcement, institutional decision safeguards, and collective judgment failure.

The examples are designed for social psychologists, political psychologists, communication researchers, organizational researchers, legal scholars, behavioral scientists, platform researchers, public-policy researchers, and scholars studying deliberation, decision-making, ideology, identity, and institutional governance.

## Research focus

The code operationalizes group-polarization and collective-judgment research through:

- participant, group, session, scenario, platform, and institution identifiers
- pre-discussion attitude
- post-discussion attitude
- attitude shift
- directional polarization
- extremity amplification
- confidence before and after discussion
- persuasive argument exposure
- argument diversity
- informational homogeneity
- social comparison pressure
- identity salience
- group identification
- norm enforcement
- dissent presence
- dissent quality
- minority-view protection
- deliberation structure
- moderation quality
- algorithmic reinforcement
- cross-cutting exposure
- perceived consensus
- perceived legitimacy
- decision quality
- collective judgment accuracy
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, polarization models, collective-judgment models, and iterative amplification simulations
- `r/` — multilevel attitude-shift, confidence, decision-quality, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — iterative group-discussion and deliberative-safeguard simulation
- `c` — fast polarization-amplification simulator
- `cpp` — deliberation-structure simulator
- `fortran` — repeated-discussion recurrence model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/group_polarization_model.py --simulate --output data/group_polarization_trials.csv --outputs outputs
python3 python/group_polarization_model.py --input data/group_polarization_trials.csv --outputs outputs
Rscript r/group_polarization_analysis.R data/group_polarization_trials.csv outputs
go run go/validator.go data/group_polarization_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/group_polarization_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/group-polarization-and-collective-judgment
