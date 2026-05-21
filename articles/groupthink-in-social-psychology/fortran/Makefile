FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: consensus_pressure_recurrence

consensus_pressure_recurrence: consensus_pressure_recurrence.f90
	$(FC) $(FFLAGS) -o consensus_pressure_recurrence consensus_pressure_recurrence.f90

run: consensus_pressure_recurrence
	./consensus_pressure_recurrence

clean:
	rm -f consensus_pressure_recurrence
