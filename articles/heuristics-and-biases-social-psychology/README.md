# Heuristics and Biases

This folder contains reproducible research code for studying heuristics, cognitive biases, bounded rationality, judgment under uncertainty, anchoring, availability, representativeness, affective judgment, framing effects, base-rate neglect, overconfidence, confirmation bias, loss aversion, calibration, social judgment, institutional decision-making, and debiasing interventions.

The examples are designed for social psychologists, behavioral economists, decision scientists, public-policy researchers, legal scholars, medical decision researchers, risk analysts, organizational researchers, and scholars studying judgment, uncertainty, cognitive shortcuts, and institutional error.

## Research focus

The code operationalizes heuristics-and-biases research through:

- participant, session, group, scenario, site, and institutional identifiers
- judgment domain
- heuristic type
- experimental condition
- anchor value
- true value
- estimate
- estimation error
- base rate
- individuating information
- representativeness rating
- availability salience
- affect valence
- perceived risk
- perceived benefit
- frame type
- gain/loss framing
- confidence rating
- actual accuracy
- calibration error
- confirmation tendency
- disconfirming evidence exposure
- overconfidence score
- response latency
- debiasing intervention strength
- institutional accountability
- decision quality

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, anchoring models, calibration models, framing models, institutional-debiasing simulation
- `r/` — multilevel anchoring, calibration, framing, availability, and response-time models
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in WordPress
- `julia/` — institutional bias accumulation and debiasing simulation
- `c` — fast anchoring simulator
- `cpp` — institutional decision-bias simulator
- `fortran` — bounded-rationality recurrence model
- `go` — CSV validation utility
- `rust` — fast heuristic-level summary utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/heuristics_biases_model.py --simulate --output data/heuristics_biases_trials.csv --outputs outputs
python3 python/heuristics_biases_model.py --input data/heuristics_biases_trials.csv --outputs outputs
Rscript r/heuristics_biases_analysis.R data/heuristics_biases_trials.csv outputs
go run go/validator.go data/heuristics_biases_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/heuristics_biases_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/heuristics-and-biases-social-psychology
