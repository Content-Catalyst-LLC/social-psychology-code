FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: norm_adoption_recurrence

norm_adoption_recurrence: norm_adoption_recurrence.f90
	$(FC) $(FFLAGS) -o norm_adoption_recurrence norm_adoption_recurrence.f90

run: norm_adoption_recurrence
	./norm_adoption_recurrence

clean:
	rm -f norm_adoption_recurrence
