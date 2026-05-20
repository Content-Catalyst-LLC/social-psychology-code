FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: situational_constraint_neglect

situational_constraint_neglect: situational_constraint_neglect.f90
	$(FC) $(FFLAGS) -o situational_constraint_neglect situational_constraint_neglect.f90

run: situational_constraint_neglect
	./situational_constraint_neglect

clean:
	rm -f situational_constraint_neglect
