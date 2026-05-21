CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: latency_difference_simulator

latency_difference_simulator: latency_difference_simulator.c
	$(CC) $(CFLAGS) -o latency_difference_simulator latency_difference_simulator.c -lm

run: latency_difference_simulator
	./latency_difference_simulator

clean:
	rm -f latency_difference_simulator
