.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-blame fortran-sim julia-sim all clean

python-generate:
	python3 python/fundamental_attribution_error_model.py --simulate --output data/fundamental_attribution_error_trials.csv --outputs outputs

python-model:
	python3 python/fundamental_attribution_error_model.py --input data/fundamental_attribution_error_trials.csv --outputs outputs

r-analysis:
	Rscript r/fundamental_attribution_error_analysis.R data/fundamental_attribution_error_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/fundamental_attribution_error_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/fundamental_attribution_error_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-blame:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia attribution_correction_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-blame fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
