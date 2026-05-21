CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: contact_intervention_simulator

contact_intervention_simulator: contact_intervention_simulator.cpp
	$(CXX) $(CXXFLAGS) -o contact_intervention_simulator contact_intervention_simulator.cpp

run: contact_intervention_simulator
	./contact_intervention_simulator ../outputs/cpp_contact_intervention_simulation.csv

clean:
	rm -f contact_intervention_simulator
