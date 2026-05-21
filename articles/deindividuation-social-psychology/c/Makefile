CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: identity_shift_simulator

identity_shift_simulator: identity_shift_simulator.c
	$(CC) $(CFLAGS) -o identity_shift_simulator identity_shift_simulator.c -lm

run: identity_shift_simulator
	./identity_shift_simulator 10000

clean:
	rm -f identity_shift_simulator
