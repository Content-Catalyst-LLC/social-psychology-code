FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: facilitation_performance_model

facilitation_performance_model: facilitation_performance_model.f90
	$(FC) $(FFLAGS) -o facilitation_performance_model facilitation_performance_model.f90

run: facilitation_performance_model
	./facilitation_performance_model

clean:
	rm -f facilitation_performance_model
