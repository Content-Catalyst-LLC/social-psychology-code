CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: institutional_conformity_simulator

institutional_conformity_simulator: institutional_conformity_simulator.cpp
	$(CXX) $(CXXFLAGS) -o institutional_conformity_simulator institutional_conformity_simulator.cpp

run: institutional_conformity_simulator
	./institutional_conformity_simulator ../outputs/cpp_institutional_conformity_simulation.csv

clean:
	rm -f institutional_conformity_simulator
