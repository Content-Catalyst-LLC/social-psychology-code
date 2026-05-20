FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: repeated_comparison_affect_model

repeated_comparison_affect_model: repeated_comparison_affect_model.f90
	$(FC) $(FFLAGS) -o repeated_comparison_affect_model repeated_comparison_affect_model.f90

run: repeated_comparison_affect_model
	./repeated_comparison_affect_model

clean:
	rm -f repeated_comparison_affect_model
