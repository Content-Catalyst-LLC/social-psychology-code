# Moral Disengagement in Social Psychology

This folder contains reproducible research code for studying moral disengagement, moral self-regulation, justificatory cognition, responsibility displacement, diffusion of responsibility, consequence distortion, dehumanization, victim blame, organizational misconduct, collective violence, and ethical-system design.

The examples are designed for social psychologists, moral psychologists, organizational-behavior researchers, political psychologists, conflict researchers, ethics researchers, and computational social scientists studying how people rationalize harmful behavior while preserving moral self-regard.

## Research focus

The code operationalizes moral disengagement through:

- participant and site identifiers
- experimental condition
- moral justification
- euphemistic labeling
- advantageous comparison
- displacement of responsibility
- diffusion of responsibility
- distortion or minimization of consequences
- dehumanization
- attribution of blame
- harm visibility
- perceived agency
- responsibility clarity
- institutional pressure
- authority pressure
- group norm strength
- victim distance
- empathy
- guilt
- harmful decision
- policy endorsement
- unethical intention
- response time

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, moral-disengagement models, harmful-choice models, and institutional-normalization simulations
- `r/` — multilevel models, disengagement indices, mechanism-specific estimates, and visualization
- `sql/` — relational schema, views, and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — repeated normalization and ethical-erosion simulation
- `c` — fast disengagement-index simulator
- `cpp` — organizational normalization simulator
- `fortran` — repeated harmful-choice simulation
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/moral_disengagement_model.py --simulate --output data/moral_disengagement_trials.csv --outputs outputs
python3 python/moral_disengagement_model.py --input data/moral_disengagement_trials.csv --outputs outputs
Rscript r/moral_disengagement_analysis.R data/moral_disengagement_trials.csv outputs
go run go/validator.go data/moral_disengagement_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/moral_disengagement_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/moral-disengagement-social-psychology
