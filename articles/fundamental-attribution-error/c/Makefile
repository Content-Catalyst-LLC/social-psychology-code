CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: dispositional_inference_simulator

dispositional_inference_simulator: dispositional_inference_simulator.c
	$(CC) $(CFLAGS) -o dispositional_inference_simulator dispositional_inference_simulator.c -lm

run: dispositional_inference_simulator
	./dispositional_inference_simulator 10000

clean:
	rm -f dispositional_inference_simulator
