FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: harmful_choice_model

harmful_choice_model: harmful_choice_model.f90
	$(FC) $(FFLAGS) -o harmful_choice_model harmful_choice_model.f90

run: harmful_choice_model
	./harmful_choice_model

clean:
	rm -f harmful_choice_model
