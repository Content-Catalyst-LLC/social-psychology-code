.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-tournament fortran-sim julia-sim all clean

python-generate:
	python3 python/prisoners_dilemma_model.py --simulate --output data/prisoners_dilemma_trials.csv --outputs outputs

python-model:
	python3 python/prisoners_dilemma_model.py --input data/prisoners_dilemma_trials.csv --outputs outputs

r-analysis:
	Rscript r/prisoners_dilemma_analysis.R data/prisoners_dilemma_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/prisoners_dilemma_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/prisoners_dilemma_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-tournament:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia iterated_prisoners_dilemma.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-tournament fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
