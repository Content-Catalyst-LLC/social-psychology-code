CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: strategy_tournament

strategy_tournament: strategy_tournament.cpp
	$(CXX) $(CXXFLAGS) -o strategy_tournament strategy_tournament.cpp

run: strategy_tournament
	./strategy_tournament ../outputs/cpp_strategy_tournament.csv

clean:
	rm -f strategy_tournament
