CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: organizational_credit_blame_simulator

organizational_credit_blame_simulator: organizational_credit_blame_simulator.cpp
	$(CXX) $(CXXFLAGS) -o organizational_credit_blame_simulator organizational_credit_blame_simulator.cpp

run: organizational_credit_blame_simulator
	./organizational_credit_blame_simulator ../outputs/cpp_organizational_credit_blame.csv

clean:
	rm -f organizational_credit_blame_simulator
