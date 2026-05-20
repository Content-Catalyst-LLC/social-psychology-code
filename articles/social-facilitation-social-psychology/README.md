# Social Facilitation in Social Psychology

This folder contains reproducible research code for studying social facilitation, social inhibition, audience effects, coaction, evaluation apprehension, distraction-conflict, task difficulty, task mastery, physiological arousal, response time, performance under observation, digital monitoring, and applied performance environments.

The examples are designed for social psychologists, cognitive scientists, organizational researchers, sport psychologists, human-computer interaction researchers, education researchers, and applied behavioral scientists.

## Research focus

The code operationalizes social facilitation research through:

- participant, session, site, and task identifiers
- audience condition
- coaction condition
- evaluation pressure
- observer expertise
- audience size
- audience valence
- task difficulty
- task mastery/practice
- dominant-response correctness
- arousal index
- distraction index
- attentional conflict
- perceived scrutiny
- baseline skill
- performance score
- accuracy
- error rate
- response time
- physiological arousal
- social anxiety
- digital monitoring condition
- task domain

## Folder structure

- `data/` — sample data, data dictionary, and expected schema
- `python/` — synthetic data generation, mixed models, arousal-performance simulation, and digital monitoring simulation
- `r/` — multilevel models, audience-by-difficulty estimates, response-time models, and visualization
- `sql/` — relational schema and example queries stored in GitHub rather than embedded in article HTML
- `julia/` — arousal and performance simulation
- `c` — fast drive-theory simulation
- `cpp` — audience-effect simulator
- `fortran` — task difficulty/arousal performance model
- `go` — CSV validation utility
- `rust` — fast summary and data-quality utility
- `notebooks` — notebook workflow scaffold
- `docs` — methodological protocol and measurement notes
- `outputs` — generated summaries and model outputs

## Example commands

From this article folder:

```bash
python3 python/social_facilitation_model.py --simulate --output data/social_facilitation_trials.csv --outputs outputs
python3 python/social_facilitation_model.py --input data/social_facilitation_trials.csv --outputs outputs
Rscript r/social_facilitation_analysis.R data/social_facilitation_trials.csv outputs
go run go/validator.go data/social_facilitation_trials.csv
cargo run --manifest-path rust/Cargo.toml -- data/social_facilitation_trials.csv
make all
```

## Repository link

Article code directory:

https://github.com/Content-Catalyst-LLC/social-psychology-code/tree/main/articles/social-facilitation-social-psychology
