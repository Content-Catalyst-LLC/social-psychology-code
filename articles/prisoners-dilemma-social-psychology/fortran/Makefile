FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: cooperation_probability_model

cooperation_probability_model: cooperation_probability_model.f90
	$(FC) $(FFLAGS) -o cooperation_probability_model cooperation_probability_model.f90

run: cooperation_probability_model
	./cooperation_probability_model

clean:
	rm -f cooperation_probability_model
