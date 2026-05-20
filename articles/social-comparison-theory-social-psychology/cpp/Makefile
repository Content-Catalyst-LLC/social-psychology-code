CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: organizational_benchmarking_simulator

organizational_benchmarking_simulator: organizational_benchmarking_simulator.cpp
	$(CXX) $(CXXFLAGS) -o organizational_benchmarking_simulator organizational_benchmarking_simulator.cpp

run: organizational_benchmarking_simulator
	./organizational_benchmarking_simulator ../outputs/cpp_organizational_benchmarking.csv

clean:
	rm -f organizational_benchmarking_simulator
