CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: authority_pressure_simulator

authority_pressure_simulator: authority_pressure_simulator.c
	$(CC) $(CFLAGS) -o authority_pressure_simulator authority_pressure_simulator.c -lm

run: authority_pressure_simulator
	./authority_pressure_simulator

clean:
	rm -f authority_pressure_simulator
