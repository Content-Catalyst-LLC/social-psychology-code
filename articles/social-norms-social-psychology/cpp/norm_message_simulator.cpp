#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + std::exp(-x));
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_norm_message_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 6.0);
    std::vector<std::string> messages = {"control", "descriptive", "injunctive", "combined", "dynamic", "correction"};

    std::ofstream out(output);
    out << "message_type,descriptive_norm,injunctive_norm,dynamic_trend,legitimacy,compliance_probability,complied\n";

    for (const auto &message : messages) {
        for (int i = 0; i < cases; ++i) {
            double descriptive = message == "descriptive" ? 72.0 :
                                 message == "combined" ? 76.0 :
                                 message == "dynamic" ? 46.0 :
                                 message == "correction" ? 58.0 : 50.0;
            double injunctive = message == "injunctive" ? 84.0 :
                                message == "combined" ? 88.0 :
                                message == "correction" ? 80.0 : 58.0;
            double trend = message == "dynamic" ? 42.0 : message == "combined" ? 10.0 : 0.0;
            double legitimacy = message == "control" ? 5.5 : 6.5;

            descriptive = std::clamp(descriptive + noise(rng), 0.0, 100.0);
            injunctive = std::clamp(injunctive + noise(rng), 0.0, 100.0);

            double prob = logistic(-4.8 + 0.028 * descriptive + 0.032 * injunctive + 0.018 * trend + 0.25 * legitimacy);
            int complied = (std::generate_canonical<double, 10>(rng) < prob) ? 1 : 0;

            out << message << "," << descriptive << "," << injunctive << "," << trend << "," << legitimacy << "," << prob << "," << complied << "\n";
        }
    }

    std::cout << "Wrote norm-message simulation to: " << output << "\n";
    return 0;
}
