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
    std::string output = "../outputs/cpp_emergency_response.csv";
    if (argc > 1) output = argv[1];

    const int n = 5000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);

    std::ofstream out(output);
    out << "case_id,bystander_count,ambiguity,evaluation,role_clarity,responsibility,intervention_probability,intervention\n";

    for (int i = 1; i <= n; ++i) {
        int bystanders = (int)(12.0 * uniform(rng));
        double ambiguity = 10.0 * uniform(rng);
        double evaluation = 10.0 * uniform(rng);
        double role = 10.0 * uniform(rng);
        double responsibility = std::clamp(7.0 + 0.40 * role - 0.70 * std::log1p((double)bystanders) - 0.25 * ambiguity - 0.20 * evaluation + noise(rng), 0.0, 10.0);
        double p = logistic(-3.5 + 0.50 * responsibility + 0.25 * role - 0.20 * ambiguity - 0.20 * evaluation);
        int intervention = uniform(rng) < p ? 1 : 0;

        out << i << "," << bystanders << "," << ambiguity << "," << evaluation << "," << role << "," << responsibility << "," << p << "," << intervention << "\n";
    }

    std::cout << "Wrote emergency response simulation to: " << output << "\n";
    return 0;
}
