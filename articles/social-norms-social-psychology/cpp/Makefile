CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: norm_message_simulator

norm_message_simulator: norm_message_simulator.cpp
	$(CXX) $(CXXFLAGS) -o norm_message_simulator norm_message_simulator.cpp

run: norm_message_simulator
	./norm_message_simulator ../outputs/cpp_norm_message_simulation.csv

clean:
	rm -f norm_message_simulator
