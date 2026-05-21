FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: cumulative_welfare_model

cumulative_welfare_model: cumulative_welfare_model.f90
	$(FC) $(FFLAGS) -o cumulative_welfare_model cumulative_welfare_model.f90

run: cumulative_welfare_model
	./cumulative_welfare_model

clean:
	rm -f cumulative_welfare_model
