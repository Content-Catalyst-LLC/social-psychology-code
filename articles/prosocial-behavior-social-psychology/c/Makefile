CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: helping_propensity_simulator

helping_propensity_simulator: helping_propensity_simulator.c
	$(CC) $(CFLAGS) -o helping_propensity_simulator helping_propensity_simulator.c -lm

run: helping_propensity_simulator
	./helping_propensity_simulator

clean:
	rm -f helping_propensity_simulator
