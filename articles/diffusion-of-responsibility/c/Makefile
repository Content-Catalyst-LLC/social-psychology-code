CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: responsibility_diffusion_simulator

responsibility_diffusion_simulator: responsibility_diffusion_simulator.c
	$(CC) $(CFLAGS) -o responsibility_diffusion_simulator responsibility_diffusion_simulator.c -lm

run: responsibility_diffusion_simulator
	./responsibility_diffusion_simulator 10000

clean:
	rm -f responsibility_diffusion_simulator
