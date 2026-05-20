CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: emergency_response_simulator

emergency_response_simulator: emergency_response_simulator.cpp
	$(CXX) $(CXXFLAGS) -o emergency_response_simulator emergency_response_simulator.cpp

run: emergency_response_simulator
	./emergency_response_simulator ../outputs/cpp_emergency_response.csv

clean:
	rm -f emergency_response_simulator
