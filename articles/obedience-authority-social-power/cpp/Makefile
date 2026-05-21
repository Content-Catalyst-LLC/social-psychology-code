CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: resistance_support_simulator

resistance_support_simulator: resistance_support_simulator.cpp
	$(CXX) $(CXXFLAGS) -o resistance_support_simulator resistance_support_simulator.cpp

run: resistance_support_simulator
	./resistance_support_simulator ../outputs/cpp_resistance_support_simulation.csv

clean:
	rm -f resistance_support_simulator
