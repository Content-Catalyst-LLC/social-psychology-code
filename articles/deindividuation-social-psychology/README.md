# Deindividuation in Social Psychology

This folder contains reproducible research code for studying deindividuation, anonymity, self-awareness, accountability, group identity salience, norm salience, crowd immersion, online disinhibition, SIDE-model dynamics, moral disengagement, responsibility diffusion, and prosocial/antisocial norm-congruent behavior.

The examples are designed for social psychologists, political psychologists, digital-platform researchers, crowd-behavior researchers, computational social scientists, organizational researchers, and communication scholars.

## Research focus

The code operationalizes deindividuation research through:

- participant, session, group, platform, and site identifiers
- anonymity condition
- identifiability
- group size
- crowd immersion
- self-awareness
- private/public self-focus
- accountability
- group identity salience
- group norm valence
- norm clarity
- norm congruence
- arousal
- emotional contagion
- responsibility diffusion
- moral disengagement
- perceived surveillance
- platform moderation visibility
- behavior score
- prosocial behavior
- antisocial behavior
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, behavior models, SIDE simulations, online anonymity simulations, and moderation visibility models
- `r/` — multilevel behavior models, mediation-style summaries, anonymity-by-norm estimates, and visualization
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — SIDE and anonymity/norm-congruence simulation
- `c` — fast identity-shift simulator
- `cpp` — crowd norm-amplification simulator
- `fortran` — personal-versus-group regulation model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/deindividuation_model.py --simulate --output data/deindividuation_trials.csv --outputs outputs
python3 python/deindividuation_model.py --input data/deindividuation_trials.csv --outputs outputs
Rscript r/deindividuation_analysis.R data/deindividuation_trials.csv outputs
go run go/validator.go data/deindividuation_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/deindividuation_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/deindividuation-social-psychology
