CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: participation_threshold_simulator

participation_threshold_simulator: participation_threshold_simulator.c
	$(CC) $(CFLAGS) -o participation_threshold_simulator participation_threshold_simulator.c -lm

run: participation_threshold_simulator
	./participation_threshold_simulator 10000

clean:
	rm -f participation_threshold_simulator
