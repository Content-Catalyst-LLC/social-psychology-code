FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: intervention_propensity_model

intervention_propensity_model: intervention_propensity_model.f90
	$(FC) $(FFLAGS) -o intervention_propensity_model intervention_propensity_model.f90

run: intervention_propensity_model
	./intervention_propensity_model

clean:
	rm -f intervention_propensity_model
