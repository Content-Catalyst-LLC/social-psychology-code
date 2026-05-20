CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: disengagement_index_simulator

disengagement_index_simulator: disengagement_index_simulator.c
	$(CC) $(CFLAGS) -o disengagement_index_simulator disengagement_index_simulator.c -lm

run: disengagement_index_simulator
	./disengagement_index_simulator 10000

clean:
	rm -f disengagement_index_simulator
