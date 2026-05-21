CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: institutional_bias_simulator

institutional_bias_simulator: institutional_bias_simulator.cpp
	$(CXX) $(CXXFLAGS) -o institutional_bias_simulator institutional_bias_simulator.cpp

run: institutional_bias_simulator
	./institutional_bias_simulator ../outputs/cpp_institutional_bias_simulation.csv

clean:
	rm -f institutional_bias_simulator
