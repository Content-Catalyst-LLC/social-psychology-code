CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: spreading_simulator

spreading_simulator: spreading_simulator.c
	$(CC) $(CFLAGS) -o spreading_simulator spreading_simulator.c -lm

run: spreading_simulator
	./spreading_simulator

clean:
	rm -f spreading_simulator
