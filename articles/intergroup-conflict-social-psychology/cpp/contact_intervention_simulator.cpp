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
    std::string output = "../outputs/cpp_contact_intervention_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::vector<std::string> conditions = {"baseline_contact", "equal_status_contact", "cooperative_contact", "superordinate_goal"};

    std::ofstream out(output);
    out << "condition,contact_quality,equal_status,common_goal,institutional_support,conflict_probability,support_for_cooperation\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double contact = condition == "baseline_contact" ? 3.5 : condition == "equal_status_contact" ? 6.5 : condition == "cooperative_contact" ? 7.5 : 8.0;
            double equal = condition == "equal_status_contact" ? 8.0 : condition == "cooperative_contact" ? 7.0 : condition == "superordinate_goal" ? 7.5 : 4.0;
            double goal = condition == "superordinate_goal" ? 9.0 : condition == "cooperative_contact" ? 7.0 : 4.0;
            double support = condition == "baseline_contact" ? 4.0 : 7.5;

            contact = std::clamp(contact + noise(rng), 0.0, 10.0);
            equal = std::clamp(equal + noise(rng), 0.0, 10.0);
            goal = std::clamp(goal + noise(rng), 0.0, 10.0);
            support = std::clamp(support + noise(rng), 0.0, 10.0);

            double conflict_prob = logistic(2.0 - 0.35*contact - 0.30*equal - 0.35*goal - 0.28*support);
            double cooperation = std::clamp(20 + 5.0*contact + 4.5*equal + 5.5*goal + 4.0*support - 30.0*conflict_prob + noise(rng)*5.0, 0.0, 100.0);

            out << condition << "," << contact << "," << equal << "," << goal << "," << support << "," << conflict_prob << "," << cooperation << "\n";
        }
    }

    std::cout << "Wrote contact intervention simulation to: " << output << "\n";
    return 0;
}
