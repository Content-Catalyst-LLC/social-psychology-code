CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: contact_network_simulator

contact_network_simulator: contact_network_simulator.cpp
	$(CXX) $(CXXFLAGS) -o contact_network_simulator contact_network_simulator.cpp

run: contact_network_simulator
	./contact_network_simulator ../outputs/cpp_contact_network.csv

clean:
	rm -f contact_network_simulator
