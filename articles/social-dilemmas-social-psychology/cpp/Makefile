CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: commons_resource_simulator

commons_resource_simulator: commons_resource_simulator.cpp
	$(CXX) $(CXXFLAGS) -o commons_resource_simulator commons_resource_simulator.cpp

run: commons_resource_simulator
	./commons_resource_simulator ../outputs/cpp_commons_simulation.csv

clean:
	rm -f commons_resource_simulator
