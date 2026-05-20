FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: identity_salience_bias_model

identity_salience_bias_model: identity_salience_bias_model.f90
	$(FC) $(FFLAGS) -o identity_salience_bias_model identity_salience_bias_model.f90

run: identity_salience_bias_model
	./identity_salience_bias_model

clean:
	rm -f identity_salience_bias_model
