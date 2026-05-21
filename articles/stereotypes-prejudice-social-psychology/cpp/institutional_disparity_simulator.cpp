#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_institutional_disparity_simulation.csv";
    if (argc > 1) output = argv[1];

    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::vector<std::string> scenarios = {"unstructured", "threat_salience", "structured_criteria", "accountability", "contact_and_structure"};

    std::ofstream out(output);
    out << "scenario,decision_id,decision_disparity,cumulative_disparity\n";

    for (const auto &scenario : scenarios) {
        double cumulative = 0.0;
        for (int i = 1; i <= 10000; ++i) {
            double mean = 0.020;
            double sd = 0.055;
            if (scenario == "threat_salience") {
                mean = 0.035; sd = 0.065;
            } else if (scenario == "structured_criteria") {
                mean = 0.006; sd = 0.035;
            } else if (scenario == "accountability") {
                mean = 0.008; sd = 0.038;
            } else if (scenario == "contact_and_structure") {
                mean = 0.002; sd = 0.030;
            }

            double disparity = mean + noise(rng) * sd;
            cumulative += disparity;

            if (i % 100 == 0) {
                out << scenario << "," << i << "," << disparity << "," << cumulative << "\n";
            }
        }
    }

    std::cout << "Wrote institutional disparity simulation to: " << output << "\n";
    return 0;
}
