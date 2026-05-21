CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: conflict_intensity_simulator

conflict_intensity_simulator: conflict_intensity_simulator.c
	$(CC) $(CFLAGS) -o conflict_intensity_simulator conflict_intensity_simulator.c -lm

run: conflict_intensity_simulator
	./conflict_intensity_simulator

clean:
	rm -f conflict_intensity_simulator
