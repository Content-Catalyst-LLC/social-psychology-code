CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: polarization_amplification_simulator

polarization_amplification_simulator: polarization_amplification_simulator.c
	$(CC) $(CFLAGS) -o polarization_amplification_simulator polarization_amplification_simulator.c -lm

run: polarization_amplification_simulator
	./polarization_amplification_simulator

clean:
	rm -f polarization_amplification_simulator
