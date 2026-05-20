#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + std::exp(-x));
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_network_cascade.csv";
    if (argc > 1) output = argv[1];

    const int n = 300;
    const int steps = 20;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);

    std::vector<double> identity(n), injustice(n), efficacy(n), cost(n), threshold(n);
    std::vector<int> active(n, 0);
    std::vector<std::vector<int>> neighbors(n);

    for (int i = 0; i < n; ++i) {
        identity[i] = 10.0 * uniform(rng);
        injustice[i] = 10.0 * uniform(rng);
        efficacy[i] = 10.0 * uniform(rng);
        cost[i] = 10.0 * uniform(rng);
        threshold[i] = 5.5 + 3.0 * uniform(rng);
        if (uniform(rng) < 0.04) active[i] = 1;
    }

    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (uniform(rng) < 0.025) {
                neighbors[i].push_back(j);
                neighbors[j].push_back(i);
            }
        }
    }

    std::ofstream out(output);
    out << "step,active_count,active_rate,newly_active\n";

    for (int step = 1; step <= steps; ++step) {
        std::vector<int> next = active;
        int newly_active = 0;

        for (int i = 0; i < n; ++i) {
            if (active[i]) continue;

            int active_neighbors = 0;
            for (int nb : neighbors[i]) {
                if (active[nb]) active_neighbors++;
            }

            double propensity = 0.22 * identity[i] + 0.22 * injustice[i] + 0.22 * efficacy[i] + 0.65 * active_neighbors - 0.20 * cost[i];

            if (propensity >= threshold[i]) {
                next[i] = 1;
                newly_active++;
            }
        }

        active = next;
        int active_count = 0;
        for (int v : active) active_count += v;

        out << step << "," << active_count << "," << (double)active_count / n << "," << newly_active << "\n";
    }

    std::cout << "Wrote network cascade simulation to: " << output << "\n";
    return 0;
}
