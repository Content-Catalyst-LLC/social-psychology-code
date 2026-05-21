#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

static double logistic(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_institutional_conformity_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::uniform_real_distribution<double> u(0.0, 1.0);
    std::vector<std::string> conditions = {"agreement_culture", "psychological_safety", "visible_dissent", "high_status_majority", "algorithmic_social_proof"};

    std::ofstream out(output);
    out << "condition,normative_pressure,unanimity,visible_dissent,status_strength,psychological_safety,social_proof,conformity_probability,conformed\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double normative = condition == "agreement_culture" ? 8.5 : condition == "psychological_safety" ? 4.0 : 6.0;
            double unanimity = condition == "visible_dissent" ? 4.0 : 8.0;
            double dissent = condition == "visible_dissent" ? 8.5 : condition == "psychological_safety" ? 7.0 : 1.8;
            double status = condition == "high_status_majority" ? 9.0 : 6.0;
            double safety = condition == "psychological_safety" ? 9.0 : condition == "agreement_culture" ? 2.5 : 5.0;
            double proof = condition == "algorithmic_social_proof" ? 9.5 : 3.5;

            normative = std::clamp(normative + noise(rng), 0.0, 10.0);
            unanimity = std::clamp(unanimity + noise(rng), 0.0, 10.0);
            dissent = std::clamp(dissent + noise(rng), 0.0, 10.0);
            status = std::clamp(status + noise(rng), 0.0, 10.0);
            safety = std::clamp(safety + noise(rng), 0.0, 10.0);
            proof = std::clamp(proof + noise(rng), 0.0, 10.0);

            double p_conform = logistic(-3.0 + 0.36*normative + 0.38*unanimity + 0.24*status + 0.22*proof - 0.42*dissent - 0.24*safety);
            int conformed = u(rng) < p_conform ? 1 : 0;

            out << condition << "," << normative << "," << unanimity << "," << dissent << "," << status << "," << safety << "," << proof << "," << p_conform << "," << conformed << "\n";
        }
    }

    std::cout << "Wrote institutional conformity simulation to: " << output << "\n";
    return 0;
}
