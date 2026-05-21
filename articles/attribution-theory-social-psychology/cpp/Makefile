CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: responsibility_simulator

responsibility_simulator: responsibility_simulator.cpp
	$(CXX) $(CXXFLAGS) -o responsibility_simulator responsibility_simulator.cpp

run: responsibility_simulator
	./responsibility_simulator ../outputs/cpp_responsibility_simulation.csv

clean:
	rm -f responsibility_simulator
