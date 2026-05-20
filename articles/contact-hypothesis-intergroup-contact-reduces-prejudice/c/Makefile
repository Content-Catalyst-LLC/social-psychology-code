CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: contact_prejudice_simulator

contact_prejudice_simulator: contact_prejudice_simulator.c
	$(CC) $(CFLAGS) -o contact_prejudice_simulator contact_prejudice_simulator.c -lm

run: contact_prejudice_simulator
	./contact_prejudice_simulator 10000

clean:
	rm -f contact_prejudice_simulator
