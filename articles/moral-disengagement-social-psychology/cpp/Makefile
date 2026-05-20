CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: organizational_normalization_simulator

organizational_normalization_simulator: organizational_normalization_simulator.cpp
	$(CXX) $(CXXFLAGS) -o organizational_normalization_simulator organizational_normalization_simulator.cpp

run: organizational_normalization_simulator
	./organizational_normalization_simulator ../outputs/cpp_organizational_normalization.csv

clean:
	rm -f organizational_normalization_simulator
