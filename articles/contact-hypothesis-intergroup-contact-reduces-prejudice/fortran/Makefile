FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: repeated_contact_model

repeated_contact_model: repeated_contact_model.f90
	$(FC) $(FFLAGS) -o repeated_contact_model repeated_contact_model.f90

run: repeated_contact_model
	./repeated_contact_model

clean:
	rm -f repeated_contact_model
