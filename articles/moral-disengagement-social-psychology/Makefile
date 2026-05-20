.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-norm fortran-sim julia-sim all clean

python-generate:
	python3 python/moral_disengagement_model.py --simulate --output data/moral_disengagement_trials.csv --outputs outputs

python-model:
	python3 python/moral_disengagement_model.py --input data/moral_disengagement_trials.csv --outputs outputs

r-analysis:
	Rscript r/moral_disengagement_analysis.R data/moral_disengagement_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/moral_disengagement_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/moral_disengagement_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-norm:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia institutional_normalization_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-norm fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
