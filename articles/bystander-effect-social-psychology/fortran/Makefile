FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: intervention_threshold_model

intervention_threshold_model: intervention_threshold_model.f90
	$(FC) $(FFLAGS) -o intervention_threshold_model intervention_threshold_model.f90

run: intervention_threshold_model
	./intervention_threshold_model

clean:
	rm -f intervention_threshold_model
