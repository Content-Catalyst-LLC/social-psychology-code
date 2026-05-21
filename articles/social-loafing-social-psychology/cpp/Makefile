CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17
all: team_accountability_simulator
team_accountability_simulator: team_accountability_simulator.cpp
	$(CXX) $(CXXFLAGS) -o team_accountability_simulator team_accountability_simulator.cpp
run: team_accountability_simulator
	./team_accountability_simulator ../outputs/cpp_team_accountability_simulation.csv
clean:
	rm -f team_accountability_simulator
