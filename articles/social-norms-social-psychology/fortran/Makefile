FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: norm_equilibrium_model

norm_equilibrium_model: norm_equilibrium_model.f90
	$(FC) $(FFLAGS) -o norm_equilibrium_model norm_equilibrium_model.f90

run: norm_equilibrium_model
	./norm_equilibrium_model

clean:
	rm -f norm_equilibrium_model
