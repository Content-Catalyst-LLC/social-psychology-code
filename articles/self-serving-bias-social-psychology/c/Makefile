CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: attribution_asymmetry_simulator

attribution_asymmetry_simulator: attribution_asymmetry_simulator.c
	$(CC) $(CFLAGS) -o attribution_asymmetry_simulator attribution_asymmetry_simulator.c -lm

run: attribution_asymmetry_simulator
	./attribution_asymmetry_simulator 10000

clean:
	rm -f attribution_asymmetry_simulator
