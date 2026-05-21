CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: threshold_conformity_simulator

threshold_conformity_simulator: threshold_conformity_simulator.c
	$(CC) $(CFLAGS) -o threshold_conformity_simulator threshold_conformity_simulator.c -lm

run: threshold_conformity_simulator
	./threshold_conformity_simulator

clean:
	rm -f threshold_conformity_simulator
