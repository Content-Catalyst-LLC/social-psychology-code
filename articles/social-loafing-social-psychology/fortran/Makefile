FC ?= gfortran
FFLAGS ?= -O2 -Wall
all: group_effort_model
group_effort_model: group_effort_model.f90
	$(FC) $(FFLAGS) -o group_effort_model group_effort_model.f90
run: group_effort_model
	./group_effort_model
clean:
	rm -f group_effort_model
