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
    std::string output = "../outputs/cpp_resistance_support_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::uniform_real_distribution<double> u(0.0, 1.0);
    std::vector<std::string> conditions = {"no_support", "peer_dissent", "high_responsibility", "whistleblower_protection", "visible_harm"};

    std::ofstream out(output);
    out << "condition,legitimacy,peer_dissent,responsibility,moral_conflict,cost_of_defiance,obedience_probability,resistance_probability,obeyed,resisted\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double legitimacy = condition == "no_support" ? 8.0 : condition == "whistleblower_protection" ? 6.0 : 7.0;
            double dissent = condition == "peer_dissent" ? 8.5 : condition == "whistleblower_protection" ? 7.5 : condition == "visible_harm" ? 5.5 : 1.5;
            double responsibility = condition == "high_responsibility" ? 8.8 : condition == "visible_harm" ? 8.2 : condition == "whistleblower_protection" ? 7.5 : 3.5;
            double moral = condition == "visible_harm" ? 8.8 : condition == "high_responsibility" ? 8.2 : condition == "peer_dissent" ? 7.5 : 5.2;
            double cost = condition == "whistleblower_protection" ? 2.0 : 5.8;

            legitimacy = std::clamp(legitimacy + noise(rng), 0.0, 10.0);
            dissent = std::clamp(dissent + noise(rng), 0.0, 10.0);
            responsibility = std::clamp(responsibility + noise(rng), 0.0, 10.0);
            moral = std::clamp(moral + noise(rng), 0.0, 10.0);
            cost = std::clamp(cost + noise(rng), 0.0, 10.0);

            double displacement = std::clamp(10.0 - responsibility, 0.0, 10.0);
            double p_obey = logistic(-2.0 + 0.42*legitimacy + 0.28*displacement + 0.18*cost - 0.38*dissent - 0.30*moral - 0.25*responsibility);
            double p_resist = logistic(-1.5 - 0.30*legitimacy - 0.25*cost + 0.45*dissent + 0.35*moral + 0.35*responsibility);
            int obeyed = u(rng) < p_obey ? 1 : 0;
            int resisted = (!obeyed && u(rng) < p_resist) ? 1 : 0;

            out << condition << "," << legitimacy << "," << dissent << "," << responsibility << "," << moral << "," << cost << "," << p_obey << "," << p_resist << "," << obeyed << "," << resisted << "\n";
        }
    }

    std::cout << "Wrote resistance-support simulation to: " << output << "\n";
    return 0;
}
