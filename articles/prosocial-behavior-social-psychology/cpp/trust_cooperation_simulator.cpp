#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + std::exp(-x));
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_trust_cooperation_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::bernoulli_distribution high_trust_condition(0.5);

    std::ofstream out(output);
    out << "condition,trust_level,institutional_legitimacy,norm_salience,efficacy_belief,helping_cost,cooperation_probability,contribution\n";

    for (int i = 0; i < cases; ++i) {
        bool high_trust = high_trust_condition(rng);
        std::string condition = high_trust ? "high_trust_high_legitimacy" : "low_trust_low_legitimacy";
        double trust = std::clamp((high_trust ? 8.0 : 3.0) + noise(rng), 0.0, 10.0);
        double legitimacy = std::clamp((high_trust ? 8.0 : 3.0) + noise(rng), 0.0, 10.0);
        double norms = std::clamp((high_trust ? 7.0 : 4.0) + noise(rng), 0.0, 10.0);
        double efficacy = std::clamp((high_trust ? 7.5 : 4.5) + noise(rng), 0.0, 10.0);
        double cost = std::clamp(4.0 + noise(rng), 0.0, 10.0);

        double prob = logistic(-4.0 + 0.30 * trust + 0.35 * legitimacy + 0.35 * norms + 0.35 * efficacy - 0.35 * cost);
        double contribution = std::clamp(8.0 + 3.0 * trust + 3.2 * legitimacy + 3.0 * norms + 3.0 * efficacy - 2.0 * cost + noise(rng) * 6.0, 0.0, 100.0);

        out << condition << "," << trust << "," << legitimacy << "," << norms << "," << efficacy << "," << cost << "," << prob << "," << contribution << "\n";
    }

    std::cout << "Wrote trust/cooperation simulation to: " << output << "\n";
    return 0;
}
