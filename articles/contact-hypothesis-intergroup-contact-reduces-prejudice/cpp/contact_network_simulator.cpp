#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_contact_network.csv";
    if (argc > 1) output = argv[1];

    const int n = 300;
    const int steps = 20;

    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);

    std::vector<int> group(n);
    std::vector<double> prejudice(n), trust(n), norm(n);
    std::vector<std::vector<int>> neighbors(n);

    for (int i = 0; i < n; ++i) {
        group[i] = uniform(rng) < 0.5 ? 0 : 1;
        prejudice[i] = 4.5 + 4.0 * uniform(rng);
        trust[i] = 2.0 + 3.0 * uniform(rng);
        norm[i] = 2.0 + 3.0 * uniform(rng);
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
    out << "step,mean_prejudice,mean_trust,mean_inclusive_norm,cross_group_contacts\n";

    for (int step = 1; step <= steps; ++step) {
        int cross_contacts = 0;

        for (int i = 0; i < n; ++i) {
            for (int j : neighbors[i]) {
                if (j <= i) continue;
                if (group[i] != group[j]) {
                    cross_contacts++;
                    double quality = uniform(rng);
                    prejudice[i] = std::max(0.0, prejudice[i] - 0.04 * quality * norm[i]);
                    prejudice[j] = std::max(0.0, prejudice[j] - 0.04 * quality * norm[j]);
                    trust[i] = std::min(10.0, trust[i] + 0.05 * quality);
                    trust[j] = std::min(10.0, trust[j] + 0.05 * quality);
                    norm[i] = std::min(10.0, norm[i] + 0.02);
                    norm[j] = std::min(10.0, norm[j] + 0.02);
                }
            }
        }

        double prejudice_sum = 0.0, trust_sum = 0.0, norm_sum = 0.0;
        for (int i = 0; i < n; ++i) {
            prejudice_sum += prejudice[i];
            trust_sum += trust[i];
            norm_sum += norm[i];
        }

        out << step << "," << prejudice_sum / n << "," << trust_sum / n << "," << norm_sum / n << "," << cross_contacts << "\n";
    }

    std::cout << "Wrote contact network simulation to: " << output << "\n";
    return 0;
}
