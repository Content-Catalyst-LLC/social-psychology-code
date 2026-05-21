CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: institutional_disparity_simulator

institutional_disparity_simulator: institutional_disparity_simulator.cpp
	$(CXX) $(CXXFLAGS) -o institutional_disparity_simulator institutional_disparity_simulator.cpp

run: institutional_disparity_simulator
	./institutional_disparity_simulator ../outputs/cpp_institutional_disparity_simulation.csv

clean:
	rm -f institutional_disparity_simulator
