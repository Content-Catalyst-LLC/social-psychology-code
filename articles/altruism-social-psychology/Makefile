.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-sim fortran-sim julia-sim all clean

python-generate:
	python3 python/altruism_model.py --simulate --output data/altruism_trials.csv --outputs outputs

python-model:
	python3 python/altruism_model.py --input data/altruism_trials.csv --outputs outputs

r-analysis:
	Rscript r/altruism_analysis.R data/altruism_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/altruism_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/altruism_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-sim:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia altruism_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-sim fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
