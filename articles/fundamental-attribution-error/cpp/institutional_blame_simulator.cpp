#include <fstream>
#include <iostream>
#include <random>
#include <string>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_institutional_blame.csv";
    if (argc > 1) output = argv[1];

    const int n = 5000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);

    std::ofstream out(output);
    out << "case_id,actual_constraint,perceived_constraint,accountability,perspective,cognitive_load,disposition,situation,blame,punishment\n";

    for (int i = 1; i <= n; ++i) {
        double actual_constraint = 10.0 * uniform(rng);
        double accountability = 10.0 * uniform(rng);
        double perspective = 10.0 * uniform(rng);
        double load = 10.0 * uniform(rng);
        double perceived = std::max(0.0, std::min(10.0, actual_constraint - 0.30 * load + 0.30 * accountability + 0.25 * perspective));
        double disposition = std::max(0.0, std::min(10.0, 5.0 + 0.35 * load - 0.30 * perceived - 0.20 * accountability + noise(rng)));
        double situation = std::max(0.0, std::min(10.0, 3.0 + 0.50 * perceived + 0.25 * accountability + 0.25 * perspective - 0.20 * load + noise(rng)));
        double blame = std::max(0.0, std::min(10.0, 2.0 + 0.60 * disposition - 0.25 * situation + noise(rng)));
        double punishment = std::max(0.0, std::min(10.0, 1.5 + 0.55 * blame + 0.20 * disposition - 0.20 * situation + noise(rng)));

        out << i << "," << actual_constraint << "," << perceived << "," << accountability << "," << perspective << "," << load << "," << disposition << "," << situation << "," << blame << "," << punishment << "\n";
    }

    std::cout << "Wrote institutional blame simulation to: " << output << "\n";
    return 0;
}
