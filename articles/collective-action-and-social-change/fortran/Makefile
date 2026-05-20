FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: efficacy_participation_model

efficacy_participation_model: efficacy_participation_model.f90
	$(FC) $(FFLAGS) -o efficacy_participation_model efficacy_participation_model.f90

run: efficacy_participation_model
	./efficacy_participation_model

clean:
	rm -f efficacy_participation_model
