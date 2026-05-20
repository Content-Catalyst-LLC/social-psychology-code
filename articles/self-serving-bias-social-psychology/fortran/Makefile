FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: repeated_attribution_model

repeated_attribution_model: repeated_attribution_model.f90
	$(FC) $(FFLAGS) -o repeated_attribution_model repeated_attribution_model.f90

run: repeated_attribution_model
	./repeated_attribution_model

clean:
	rm -f repeated_attribution_model
