CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: institutional_threshold_simulator

institutional_threshold_simulator: institutional_threshold_simulator.cpp
	$(CXX) $(CXXFLAGS) -o institutional_threshold_simulator institutional_threshold_simulator.cpp

run: institutional_threshold_simulator
	./institutional_threshold_simulator ../outputs/cpp_institutional_threshold_simulation.csv

clean:
	rm -f institutional_threshold_simulator
