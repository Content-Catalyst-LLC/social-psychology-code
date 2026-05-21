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
    std::string output = "../outputs/cpp_responsibility_assignment_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 0.8);
    std::vector<std::string> conditions = {"large_group", "direct_assignment", "shared_identity", "trained_bystander"};

    std::ofstream out(output);
    out << "condition,perceived_bystanders,direct_assignment,shared_identity,competence,diffusion_responsibility,felt_responsibility,intervention_probability\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            int bystanders = condition == "trained_bystander" ? 30 : 12;
            int direct = (condition == "direct_assignment" || condition == "trained_bystander") ? 1 : 0;
            double identity = condition == "shared_identity" ? 8.0 : condition == "trained_bystander" ? 6.0 : 4.0;
            double competence = condition == "trained_bystander" ? 8.5 : 6.0;
            double diffusion = std::clamp(1.0 + 1.25 * std::log1p((double)bystanders) - 2.5 * direct - 0.4 * identity + noise(rng), 0.0, 10.0);
            double responsibility = std::clamp(8.5 - 0.80 * diffusion + 1.8 * direct + 0.35 * identity + noise(rng), 0.0, 10.0);
            double prob = logistic(-4.0 + 0.55 * responsibility + 0.35 * 8.0 + 0.30 * competence - 0.40 * diffusion);

            out << condition << "," << bystanders << "," << direct << "," << identity << "," << competence << "," << diffusion << "," << responsibility << "," << prob << "\n";
        }
    }

    std::cout << "Wrote responsibility-assignment simulation to: " << output << "\n";
    return 0;
}
