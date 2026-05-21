CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: public_goods_altruism_simulator

public_goods_altruism_simulator: public_goods_altruism_simulator.cpp
	$(CXX) $(CXXFLAGS) -o public_goods_altruism_simulator public_goods_altruism_simulator.cpp

run: public_goods_altruism_simulator
	./public_goods_altruism_simulator ../outputs/cpp_public_goods_altruism_simulation.csv

clean:
	rm -f public_goods_altruism_simulator
