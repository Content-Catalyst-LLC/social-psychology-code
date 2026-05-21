FC ?= gfortran
FFLAGS ?= -O2 -Wall

all: cumulative_disparity

cumulative_disparity: cumulative_disparity.f90
	$(FC) $(FFLAGS) -o cumulative_disparity cumulative_disparity.f90

run: cumulative_disparity
	./cumulative_disparity

clean:
	rm -f cumulative_disparity
