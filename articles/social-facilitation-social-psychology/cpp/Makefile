CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: audience_effect_simulator

audience_effect_simulator: audience_effect_simulator.cpp
	$(CXX) $(CXXFLAGS) -o audience_effect_simulator audience_effect_simulator.cpp

run: audience_effect_simulator
	./audience_effect_simulator ../outputs/cpp_audience_effect_simulation.csv

clean:
	rm -f audience_effect_simulator
