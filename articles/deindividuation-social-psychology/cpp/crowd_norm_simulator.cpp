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
    std::string output = "../outputs/cpp_crowd_norm_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::vector<std::string> conditions = {"identified", "anonymous_prosocial_norm", "anonymous_antisocial_norm", "moderated_platform"};

    std::ofstream out(output);
    out << "condition,anonymity,group_identity_salience,group_norm_valence,accountability,norm_clarity,lambda_group,norm_congruence,prosocial_behavior,antisocial_behavior\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double anonymity = condition == "identified" ? 1.5 : condition == "moderated_platform" ? 6.0 : 8.5;
            double group_identity = condition == "identified" ? 3.0 : condition == "moderated_platform" ? 7.0 : 8.0;
            double norm_valence = condition == "anonymous_antisocial_norm" ? -4.0 : condition == "identified" ? 0.0 : 4.0;
            double accountability = condition == "identified" ? 8.0 : condition == "moderated_platform" ? 7.0 : 2.5;
            double norm_clarity = condition == "identified" ? 3.0 : 8.0;

            anonymity += noise(rng) * 0.8;
            group_identity += noise(rng) * 0.8;
            norm_valence += noise(rng) * 0.8;
            accountability += noise(rng) * 0.8;
            norm_clarity += noise(rng) * 0.8;

            double lambda_group = logistic(-2.0 + 0.32 * anonymity + 0.30 * group_identity + 0.18 * norm_clarity - 0.20 * accountability);
            double norm_congruence = std::clamp(2.0 + 7.0 * lambda_group + noise(rng) * 0.9, 0.0, 10.0);
            double prosocial = std::clamp(40.0 + 7.0 * std::max(norm_valence, 0.0) + 2.5 * norm_congruence * (norm_valence > 0) + accountability + noise(rng) * 6.0, 0.0, 100.0);
            double antisocial = std::clamp(20.0 + 8.0 * std::max(-norm_valence, 0.0) + 2.8 * norm_congruence * (norm_valence < 0) - 1.3 * accountability + noise(rng) * 6.0, 0.0, 100.0);

            out << condition << "," << anonymity << "," << group_identity << "," << norm_valence << ","
                << accountability << "," << norm_clarity << "," << lambda_group << ","
                << norm_congruence << "," << prosocial << "," << antisocial << "\n";
        }
    }

    std::cout << "Wrote crowd norm simulation to: " << output << "\n";
    return 0;
}
