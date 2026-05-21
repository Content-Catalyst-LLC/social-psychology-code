#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_institutional_threshold_simulation.csv";
    if (argc > 1) output = argv[1];

    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::uniform_real_distribution<double> u(0.0, 1.0);
    std::vector<std::string> scenarios = {"unstructured", "time_pressure", "accountability", "structured_review", "blind_review"};

    std::ofstream out(output);
    out << "scenario,decision_id,score,threshold,selected\n";

    for (const auto &scenario : scenarios) {
        for (int i = 1; i <= 10000; ++i) {
            double base = 70.0 + noise(rng) * 12.0;
            double threshold = 70.0;

            if (scenario == "time_pressure") {
                base -= 2.5;
            } else if (scenario == "accountability") {
                base -= 0.8;
            } else if (scenario == "structured_review") {
                base -= 0.2;
            } else if (scenario == "blind_review") {
                base += 0.0;
            } else {
                base -= 1.6;
            }

            int selected = base >= threshold ? 1 : 0;
            out << scenario << "," << i << "," << base << "," << threshold << "," << selected << "\n";
        }
    }

    std::cout << "Wrote institutional threshold simulation to: " << output << "\n";
    return 0;
}
