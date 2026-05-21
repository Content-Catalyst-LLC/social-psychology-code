CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: groupthink_risk_simulator

groupthink_risk_simulator: groupthink_risk_simulator.c
	$(CC) $(CFLAGS) -o groupthink_risk_simulator groupthink_risk_simulator.c -lm

run: groupthink_risk_simulator
	./groupthink_risk_simulator

clean:
	rm -f groupthink_risk_simulator
