CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: policy_rationalization_simulator

policy_rationalization_simulator: policy_rationalization_simulator.cpp
	$(CXX) $(CXXFLAGS) -o policy_rationalization_simulator policy_rationalization_simulator.cpp

run: policy_rationalization_simulator
	./policy_rationalization_simulator ../outputs/cpp_policy_rationalization_simulation.csv

clean:
	rm -f policy_rationalization_simulator
