CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: comparison_gap_simulator

comparison_gap_simulator: comparison_gap_simulator.c
	$(CC) $(CFLAGS) -o comparison_gap_simulator comparison_gap_simulator.c -lm

run: comparison_gap_simulator
	./comparison_gap_simulator 10000

clean:
	rm -f comparison_gap_simulator
