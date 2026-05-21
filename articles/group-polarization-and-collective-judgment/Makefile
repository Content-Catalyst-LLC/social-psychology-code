.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-sim fortran-sim julia-sim all clean

python-generate:
	python3 python/group_polarization_model.py --simulate --output data/group_polarization_trials.csv --outputs outputs

python-model:
	python3 python/group_polarization_model.py --input data/group_polarization_trials.csv --outputs outputs

r-analysis:
	Rscript r/group_polarization_analysis.R data/group_polarization_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/group_polarization_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/group_polarization_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-sim:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia repeated_discussion_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-sim fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
