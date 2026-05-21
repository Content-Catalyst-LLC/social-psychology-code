CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: crowd_norm_simulator

crowd_norm_simulator: crowd_norm_simulator.cpp
	$(CXX) $(CXXFLAGS) -o crowd_norm_simulator crowd_norm_simulator.cpp

run: crowd_norm_simulator
	./crowd_norm_simulator ../outputs/cpp_crowd_norm_simulation.csv

clean:
	rm -f crowd_norm_simulator
