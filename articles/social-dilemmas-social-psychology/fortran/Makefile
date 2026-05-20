FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: contribution_probability_model

contribution_probability_model: contribution_probability_model.f90
	$(FC) $(FFLAGS) -o contribution_probability_model contribution_probability_model.f90

run: contribution_probability_model
	./contribution_probability_model

clean:
	rm -f contribution_probability_model
