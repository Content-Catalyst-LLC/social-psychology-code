.PHONY: python-generate python-model r-analysis go-validate rust-summary c-threshold cpp-cascade fortran-efficacy julia-threshold all clean

python-generate:
	python3 python/collective_action_model.py --simulate --output data/collective_action_trials.csv --outputs outputs

python-model:
	python3 python/collective_action_model.py --input data/collective_action_trials.csv --outputs outputs

r-analysis:
	Rscript r/collective_action_analysis.R data/collective_action_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/collective_action_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/collective_action_trials.csv

c-threshold:
	$(MAKE) -C c run

cpp-cascade:
	$(MAKE) -C cpp run

fortran-efficacy:
	$(MAKE) -C fortran run

julia-threshold:
	cd julia && julia threshold_mobilization_simulation.jl

all: python-generate python-model go-validate rust-summary c-threshold cpp-cascade fortran-efficacy

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
