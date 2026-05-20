#include <fstream>
#include <iostream>
#include <random>
#include <string>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_organizational_credit_blame.csv";
    if (argc > 1) output = argv[1];

    const int n = 5000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);

    std::ofstream out(output);
    out << "project_id,success,ego_threat,evidence_strength,accountability,credit_claiming,excuse_making,learning\n";

    for (int i = 1; i <= n; ++i) {
        int success = uniform(rng) < 0.5 ? 1 : 0;
        double ego_threat = 10.0 * uniform(rng);
        double evidence = 10.0 * uniform(rng);
        double accountability = 10.0 * uniform(rng);

        double credit = std::max(0.0, std::min(10.0, 2.0 + 5.0 * success + 0.20 * ego_threat - 0.20 * accountability + noise(rng)));
        double excuse = std::max(0.0, std::min(10.0, 2.0 + 5.0 * (1 - success) + 0.35 * ego_threat - 0.35 * accountability - 0.25 * evidence + noise(rng)));
        double learning = std::max(0.0, std::min(10.0, 4.0 + 0.40 * accountability + 0.35 * evidence - 0.40 * excuse + noise(rng)));

        out << i << "," << success << "," << ego_threat << "," << evidence << "," << accountability << "," << credit << "," << excuse << "," << learning << "\n";
    }

    std::cout << "Wrote organizational credit/blame simulation to: " << output << "\n";
    return 0;
}
