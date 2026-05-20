CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: network_cascade_simulator

network_cascade_simulator: network_cascade_simulator.cpp
	$(CXX) $(CXXFLAGS) -o network_cascade_simulator network_cascade_simulator.cpp

run: network_cascade_simulator
	./network_cascade_simulator ../outputs/cpp_network_cascade.csv

clean:
	rm -f network_cascade_simulator
