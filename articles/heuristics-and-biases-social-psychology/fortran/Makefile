FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: bounded_rationality_recurrence

bounded_rationality_recurrence: bounded_rationality_recurrence.f90
	$(FC) $(FFLAGS) -o bounded_rationality_recurrence bounded_rationality_recurrence.f90

run: bounded_rationality_recurrence
	./bounded_rationality_recurrence

clean:
	rm -f bounded_rationality_recurrence
