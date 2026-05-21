.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-sim fortran-sim julia-sim all clean

python-generate:
	python3 python/implicit_bias_model.py --simulate --output data/implicit_bias_trials.csv --outputs outputs

python-model:
	python3 python/implicit_bias_model.py --input data/implicit_bias_trials.csv --outputs outputs

r-analysis:
	Rscript r/implicit_bias_analysis.R data/implicit_bias_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/implicit_bias_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/implicit_bias_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-sim:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia institutional_disparity_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-sim fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
