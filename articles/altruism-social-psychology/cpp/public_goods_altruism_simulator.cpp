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
    std::string output = "../outputs/cpp_public_goods_altruism_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::bernoulli_distribution group_condition(0.5);

    std::ofstream out(output);
    out << "condition,empathy_score,social_norm_salience,perceived_efficacy,moral_identity,helping_cost,contribution,altruistic_decision\n";

    for (int i = 0; i < cases; ++i) {
        bool strong_norm = group_condition(rng);
        std::string condition = strong_norm ? "strong_public_good_norm" : "weak_public_good_norm";
        double empathy = std::clamp(6.0 + noise(rng), 0.0, 10.0);
        double norm = std::clamp((strong_norm ? 8.0 : 3.0) + noise(rng), 0.0, 10.0);
        double efficacy = std::clamp((strong_norm ? 8.0 : 4.0) + noise(rng), 0.0, 10.0);
        double moral = std::clamp(6.0 + noise(rng), 0.0, 10.0);
        double cost = std::clamp(4.0 + noise(rng), 0.0, 10.0);

        double prob = logistic(-4.0 + 0.25 * empathy + 0.35 * norm + 0.40 * efficacy + 0.35 * moral - 0.35 * cost);
        int decision = (std::generate_canonical<double, 10>(rng) < prob) ? 1 : 0;
        double contribution = std::clamp(10.0 + 8.0 * decision + 3.0 * norm + 3.0 * efficacy + 2.0 * moral - 2.0 * cost + noise(rng) * 6.0, 0.0, 100.0);

        out << condition << "," << empathy << "," << norm << "," << efficacy << "," << moral << "," << cost << "," << contribution << "," << decision << "\n";
    }

    std::cout << "Wrote public-goods altruism simulation to: " << output << "\n";
    return 0;
}
