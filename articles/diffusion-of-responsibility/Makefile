.PHONY: python-generate python-model r-analysis go-validate rust-summary c-sim cpp-emergency fortran-sim julia-sim all clean

python-generate:
	python3 python/diffusion_responsibility_model.py --simulate --output data/diffusion_responsibility_trials.csv --outputs outputs

python-model:
	python3 python/diffusion_responsibility_model.py --input data/diffusion_responsibility_trials.csv --outputs outputs

r-analysis:
	Rscript r/diffusion_responsibility_analysis.R data/diffusion_responsibility_trials.csv outputs

go-validate:
	cd go && go run validator.go ../data/diffusion_responsibility_trials.csv

rust-summary:
	cargo run --manifest-path rust/Cargo.toml -- data/diffusion_responsibility_trials.csv

c-sim:
	$(MAKE) -C c run

cpp-emergency:
	$(MAKE) -C cpp run

fortran-sim:
	$(MAKE) -C fortran run

julia-sim:
	cd julia && julia organizational_fragmentation_simulation.jl

all: python-generate python-model go-validate rust-summary c-sim cpp-emergency fortran-sim

clean:
	$(MAKE) -C c clean
	$(MAKE) -C cpp clean
	$(MAKE) -C fortran clean
	rm -f outputs/*.csv outputs/*.txt outputs/*.png
