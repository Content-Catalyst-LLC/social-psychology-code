FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: commons_stock_model

commons_stock_model: commons_stock_model.f90
	$(FC) $(FFLAGS) -o commons_stock_model commons_stock_model.f90

run: commons_stock_model
	./commons_stock_model

clean:
	rm -f commons_stock_model
