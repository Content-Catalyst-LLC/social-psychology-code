.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-commons fortran-sim julia-sim all clean

python-generate:
	python3 python/tragedy_commons_model.py --simulate --output data/tragedy_commons_trials.csv --outputs outputs

python-model:
	python3 python/tragedy_commons_model.py --input data/tragedy_commons_trials.csv --outputs outputs

r-analysis:
	Rscript r/tragedy_commons_analysis.R data/tragedy_commons_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/tragedy_commons_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/tragedy_commons_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-commons:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia commons_governance_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-commons fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
