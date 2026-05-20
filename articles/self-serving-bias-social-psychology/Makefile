.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-org fortran-sim julia-sim all clean

python-generate:
	python3 python/self_serving_bias_model.py --simulate --output data/self_serving_bias_trials.csv --outputs outputs

python-model:
	python3 python/self_serving_bias_model.py --input data/self_serving_bias_trials.csv --outputs outputs

r-analysis:
	Rscript r/self_serving_bias_analysis.R data/self_serving_bias_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/self_serving_bias_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/self_serving_bias_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-org:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia self_serving_bias_repeated_outcomes.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-org fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
