#include <fstream>
#include <iostream>
#include <random>
#include <string>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_minimal_group_allocation.csv";
    if (argc > 1) output = argv[1];

    const int n = 5000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 5.0);

    std::ofstream out(output);
    out << "case_id,ingroup_target,identity_salience,threat,resource_allocation,trust_rating,moral_blame\n";

    for (int i = 1; i <= n; ++i) {
        int ingroup = uniform(rng) < 0.5 ? 1 : 0;
        double identity = 10.0 * uniform(rng);
        double threat = 10.0 * uniform(rng);
        double bias = ingroup ? (0.30 * identity + 0.22 * threat) : (-0.12 * threat);
        double allocation = std::max(0.0, std::min(100.0, 50.0 + 4.5 * bias + noise(rng)));
        double trust = std::max(0.0, std::min(10.0, 5.0 + 0.55 * bias + 0.2 * noise(rng)));
        double blame = std::max(0.0, std::min(10.0, 5.0 - 0.45 * bias + 0.18 * threat + 0.2 * noise(rng)));

        out << i << "," << ingroup << "," << identity << "," << threat << "," << allocation << "," << trust << "," << blame << "\n";
    }

    std::cout << "Wrote minimal-group allocation simulation to: " << output << "\n";
    return 0;
}
