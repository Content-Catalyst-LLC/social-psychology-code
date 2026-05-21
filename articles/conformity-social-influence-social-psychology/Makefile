.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-sim fortran-sim julia-sim all clean

python-generate:
	python3 python/conformity_social_influence_model.py --simulate --output data/conformity_trials.csv --outputs outputs

python-model:
	python3 python/conformity_social_influence_model.py --input data/conformity_trials.csv --outputs outputs

r-analysis:
	Rscript r/conformity_social_influence_analysis.R data/conformity_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/conformity_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/conformity_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-sim:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia network_conformity_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-sim fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
