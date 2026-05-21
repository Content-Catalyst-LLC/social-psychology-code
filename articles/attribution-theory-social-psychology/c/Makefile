CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: covariation_simulator

covariation_simulator: covariation_simulator.c
	$(CC) $(CFLAGS) -o covariation_simulator covariation_simulator.c -lm

run: covariation_simulator
	./covariation_simulator

clean:
	rm -f covariation_simulator
