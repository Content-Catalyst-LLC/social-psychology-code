CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: drive_theory_simulator

drive_theory_simulator: drive_theory_simulator.c
	$(CC) $(CFLAGS) -o drive_theory_simulator drive_theory_simulator.c -lm

run: drive_theory_simulator
	./drive_theory_simulator 10000

clean:
	rm -f drive_theory_simulator
