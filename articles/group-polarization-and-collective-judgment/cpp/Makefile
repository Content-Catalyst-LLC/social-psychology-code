CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: deliberation_structure_simulator

deliberation_structure_simulator: deliberation_structure_simulator.cpp
	$(CXX) $(CXXFLAGS) -o deliberation_structure_simulator deliberation_structure_simulator.cpp

run: deliberation_structure_simulator
	./deliberation_structure_simulator ../outputs/cpp_deliberation_structure_simulation.csv

clean:
	rm -f deliberation_structure_simulator
