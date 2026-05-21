FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: hamilton_rule_model

hamilton_rule_model: hamilton_rule_model.f90
	$(FC) $(FFLAGS) -o hamilton_rule_model hamilton_rule_model.f90

run: hamilton_rule_model
	./hamilton_rule_model

clean:
	rm -f hamilton_rule_model
