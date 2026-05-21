FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: regulation_weight_model

regulation_weight_model: regulation_weight_model.f90
	$(FC) $(FFLAGS) -o regulation_weight_model regulation_weight_model.f90

run: regulation_weight_model
	./regulation_weight_model

clean:
	rm -f regulation_weight_model
