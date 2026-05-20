.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-minimal fortran-sim julia-sim all clean

python-generate:
	python3 python/ingroup_bias_model.py --simulate --output data/ingroup_bias_trials.csv --outputs outputs

python-model:
	python3 python/ingroup_bias_model.py --input data/ingroup_bias_trials.csv --outputs outputs

r-analysis:
	Rscript r/ingroup_bias_analysis.R data/ingroup_bias_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/ingroup_bias_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/ingroup_bias_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-minimal:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia ingroup_bias_allocation_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-minimal fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
