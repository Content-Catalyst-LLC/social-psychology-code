CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: institutional_safeguard_simulator

institutional_safeguard_simulator: institutional_safeguard_simulator.cpp
	$(CXX) $(CXXFLAGS) -o institutional_safeguard_simulator institutional_safeguard_simulator.cpp

run: institutional_safeguard_simulator
	./institutional_safeguard_simulator ../outputs/cpp_institutional_safeguard_simulation.csv

clean:
	rm -f institutional_safeguard_simulator
