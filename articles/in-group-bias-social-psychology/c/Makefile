CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: bias_differential_simulator

bias_differential_simulator: bias_differential_simulator.c
	$(CC) $(CFLAGS) -o bias_differential_simulator bias_differential_simulator.c -lm

run: bias_differential_simulator
	./bias_differential_simulator 10000

clean:
	rm -f bias_differential_simulator
