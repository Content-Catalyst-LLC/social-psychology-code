FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: escalation_recurrence_model

escalation_recurrence_model: escalation_recurrence_model.f90
	$(FC) $(FFLAGS) -o escalation_recurrence_model escalation_recurrence_model.f90

run: escalation_recurrence_model
	./escalation_recurrence_model

clean:
	rm -f escalation_recurrence_model
