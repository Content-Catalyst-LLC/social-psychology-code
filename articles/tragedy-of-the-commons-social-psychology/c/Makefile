CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: open_access_depletion_simulator

open_access_depletion_simulator: open_access_depletion_simulator.c
	$(CC) $(CFLAGS) -o open_access_depletion_simulator open_access_depletion_simulator.c -lm

run: open_access_depletion_simulator
	./open_access_depletion_simulator 60

clean:
	rm -f open_access_depletion_simulator
