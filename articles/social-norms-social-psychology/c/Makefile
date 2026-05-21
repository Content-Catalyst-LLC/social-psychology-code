CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: norm_threshold_simulator

norm_threshold_simulator: norm_threshold_simulator.c
	$(CC) $(CFLAGS) -o norm_threshold_simulator norm_threshold_simulator.c -lm

run: norm_threshold_simulator
	./norm_threshold_simulator

clean:
	rm -f norm_threshold_simulator
