CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: responsibility_assignment_simulator

responsibility_assignment_simulator: responsibility_assignment_simulator.cpp
	$(CXX) $(CXXFLAGS) -o responsibility_assignment_simulator responsibility_assignment_simulator.cpp

run: responsibility_assignment_simulator
	./responsibility_assignment_simulator ../outputs/cpp_responsibility_assignment_simulation.csv

clean:
	rm -f responsibility_assignment_simulator
