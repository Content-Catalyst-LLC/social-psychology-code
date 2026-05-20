CXX ?= c++
CXXFLAGS ?= -O2 -Wall -Wextra -std=c++17

all: minimal_group_allocation

minimal_group_allocation: minimal_group_allocation.cpp
	$(CXX) $(CXXFLAGS) -o minimal_group_allocation minimal_group_allocation.cpp

run: minimal_group_allocation
	./minimal_group_allocation ../outputs/cpp_minimal_group_allocation.csv

clean:
	rm -f minimal_group_allocation
