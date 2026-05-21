FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: attribution_expectation_recurrence

attribution_expectation_recurrence: attribution_expectation_recurrence.f90
	$(FC) $(FFLAGS) -o attribution_expectation_recurrence attribution_expectation_recurrence.f90

run: attribution_expectation_recurrence
	./attribution_expectation_recurrence

clean:
	rm -f attribution_expectation_recurrence
