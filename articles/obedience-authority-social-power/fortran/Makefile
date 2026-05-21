FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: escalation_recurrence

escalation_recurrence: escalation_recurrence.f90
	$(FC) $(FFLAGS) -o escalation_recurrence escalation_recurrence.f90

run: escalation_recurrence
	./escalation_recurrence

clean:
	rm -f escalation_recurrence
