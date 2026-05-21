FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: coherence_pressure_recurrence

coherence_pressure_recurrence: coherence_pressure_recurrence.f90
	$(FC) $(FFLAGS) -o coherence_pressure_recurrence coherence_pressure_recurrence.f90

run: coherence_pressure_recurrence
	./coherence_pressure_recurrence

clean:
	rm -f coherence_pressure_recurrence
