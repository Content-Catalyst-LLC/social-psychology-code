#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <algorithm>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + std::exp(-x));
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_organizational_normalization.csv";
    if (argc > 1) output = argv[1];

    const int n = 250;
    const int periods = 40;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);

    std::vector<double> normalized_harm(n), accountability(n), dissent(n), reward(n);
    for (int i = 0; i < n; ++i) {
        normalized_harm[i] = 0.5 + 1.5 * uniform(rng);
        accountability[i] = 2.0 + 6.0 * uniform(rng);
        dissent[i] = 2.0 + 6.0 * uniform(rng);
        reward[i] = 1.0 + 7.0 * uniform(rng);
    }

    std::ofstream out(output);
    out << "institution_id,period,moral_disengagement,harmful_rate,normalized_harm,accountability,dissent_protection,reward_for_harm\n";

    for (int t = 1; t <= periods; ++t) {
        for (int i = 0; i < n; ++i) {
            double md = std::clamp(
                2.5 + 0.35 * normalized_harm[i] + 0.35 * reward[i] -
                0.25 * accountability[i] - 0.25 * dissent[i] + 0.8 * noise(rng),
                0.0, 10.0
            );

            double harmful_rate = logistic(-3.0 + 0.55 * md + 0.25 * reward[i] - 0.28 * accountability[i]);

            normalized_harm[i] = std::clamp(
                normalized_harm[i] + 0.18 * md + 0.22 * reward[i] -
                0.25 * accountability[i] - 0.20 * dissent[i] + 0.45 * noise(rng),
                0.0, 10.0
            );

            out << (i + 1) << "," << t << "," << md << "," << harmful_rate << ","
                << normalized_harm[i] << "," << accountability[i] << "," << dissent[i]
                << "," << reward[i] << "\n";
        }
    }

    std::cout << "Wrote organizational normalization simulation to: " << output << "\n";
    return 0;
}
