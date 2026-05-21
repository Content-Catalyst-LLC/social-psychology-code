CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: costly_helping_simulator

costly_helping_simulator: costly_helping_simulator.c
	$(CC) $(CFLAGS) -o costly_helping_simulator costly_helping_simulator.c -lm

run: costly_helping_simulator
	./costly_helping_simulator

clean:
	rm -f costly_helping_simulator
