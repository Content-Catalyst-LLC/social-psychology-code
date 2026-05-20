CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: institutional_blame_simulator

institutional_blame_simulator: institutional_blame_simulator.cpp
	$(CXX) $(CXXFLAGS) -o institutional_blame_simulator institutional_blame_simulator.cpp

run: institutional_blame_simulator
	./institutional_blame_simulator ../outputs/cpp_institutional_blame.csv

clean:
	rm -f institutional_blame_simulator
