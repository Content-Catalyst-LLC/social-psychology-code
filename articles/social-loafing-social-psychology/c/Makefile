CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11
all: ringelmann_effort_simulator
ringelmann_effort_simulator: ringelmann_effort_simulator.c
	$(CC) $(CFLAGS) -o ringelmann_effort_simulator ringelmann_effort_simulator.c -lm
run: ringelmann_effort_simulator
	./ringelmann_effort_simulator 12
clean:
	rm -f ringelmann_effort_simulator
