CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: illusory_correlation_simulator

illusory_correlation_simulator: illusory_correlation_simulator.c
	$(CC) $(CFLAGS) -o illusory_correlation_simulator illusory_correlation_simulator.c -lm

run: illusory_correlation_simulator
	./illusory_correlation_simulator

clean:
	rm -f illusory_correlation_simulator
