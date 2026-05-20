CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: commons_governance_simulator

commons_governance_simulator: commons_governance_simulator.cpp
	$(CXX) $(CXXFLAGS) -o commons_governance_simulator commons_governance_simulator.cpp

run: commons_governance_simulator
	./commons_governance_simulator ../outputs/cpp_commons_governance_simulation.csv

clean:
	rm -f commons_governance_simulator
