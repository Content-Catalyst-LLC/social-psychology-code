CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: helping_probability_simulator

helping_probability_simulator: helping_probability_simulator.c
	$(CC) $(CFLAGS) -o helping_probability_simulator helping_probability_simulator.c -lm

run: helping_probability_simulator
	./helping_probability_simulator 50

clean:
	rm -f helping_probability_simulator
