CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11

all: public_goods_simulator

public_goods_simulator: public_goods_simulator.c
	$(CC) $(CFLAGS) -o public_goods_simulator public_goods_simulator.c -lm

run: public_goods_simulator
	./public_goods_simulator 10000

clean:
	rm -f public_goods_simulator
