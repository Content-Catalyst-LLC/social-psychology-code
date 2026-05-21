FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: repeated_discussion_recurrence

repeated_discussion_recurrence: repeated_discussion_recurrence.f90
	$(FC) $(FFLAGS) -o repeated_discussion_recurrence repeated_discussion_recurrence.f90

run: repeated_discussion_recurrence
	./repeated_discussion_recurrence

clean:
	rm -f repeated_discussion_recurrence
