# Conformity and Social Influence

This folder contains reproducible research code for studying conformity, normative influence, informational influence, unanimity, dissent, ambiguity, cohesion, status strength, public response, network exposure, digital social proof, and institutional conformity.

The examples are designed for social psychologists, communication researchers, organizational researchers, network scientists, behavioral economists, political psychologists, platform researchers, and scholars studying norms, social influence, and collective behavior.

## Research focus

The code operationalizes conformity research through:

- participant, group, session, scenario, site, and platform identifiers
- ambiguity
- majority size
- unanimity
- visible dissent
- ally presence
- cohesion
- normative pressure
- informational uncertainty
- status strength
- public response
- private response
- group identification
- social identity salience
- minority consistency
- network exposure
- social proof metrics
- algorithmic amplification
- conformity outcome
- resistance/dissent outcome
- confidence shift
- response time
- norm adoption over time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, conformity models, network-diffusion simulations, and social-proof simulations
- `r/` — multilevel conformity, response-time, dissent, and condition-effect models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — network conformity and norm-diffusion simulation
- `c` — fast threshold-conformity simulator
- `cpp` — institutional conformity-risk simulator
- `fortran` — repeated norm-adoption recurrence model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/conformity_social_influence_model.py --simulate --output data/conformity_trials.csv --outputs outputs
python3 python/conformity_social_influence_model.py --input data/conformity_trials.csv --outputs outputs
Rscript r/conformity_social_influence_analysis.R data/conformity_trials.csv outputs
go run go/validator.go data/conformity_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/conformity_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/conformity-social-influence-social-psychology
