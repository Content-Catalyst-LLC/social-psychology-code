.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-network fortran-repeated julia-longitudinal all clean

python-generate:
	python3 python/contact_hypothesis_model.py --simulate --output data/contact_hypothesis_trials.csv --outputs outputs

python-model:
	python3 python/contact_hypothesis_model.py --input data/contact_hypothesis_trials.csv --outputs outputs

r-analysis:
	Rscript r/contact_hypothesis_analysis.R data/contact_hypothesis_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/contact_hypothesis_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/contact_hypothesis_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-network:
	$(MAKE) -C cpp run

fortran-repeated:
	$(MAKE) -C fortran run

julia-longitudinal:
	cd julia && julia contact_longitudinal_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-network fortran-repeated

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
