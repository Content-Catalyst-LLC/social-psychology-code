CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: trust_cooperation_simulator

trust_cooperation_simulator: trust_cooperation_simulator.cpp
	$(CXX) $(CXXFLAGS) -o trust_cooperation_simulator trust_cooperation_simulator.cpp

run: trust_cooperation_simulator
	./trust_cooperation_simulator ../outputs/cpp_trust_cooperation_simulation.csv

clean:
	rm -f trust_cooperation_simulator
