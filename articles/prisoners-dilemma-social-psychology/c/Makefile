CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: repeated_pd_simulator

repeated_pd_simulator: repeated_pd_simulator.c
	$(CC) $(CFLAGS) -o repeated_pd_simulator repeated_pd_simulator.c -lm

run: repeated_pd_simulator
	./repeated_pd_simulator 10000

clean:
	rm -f repeated_pd_simulator
