#include <fstream>
#include <iostream>
#include <random>
#include <string>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_organizational_benchmarking.csv";
    if (argc > 1) output = argv[1];

    const int n = 2000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);

    std::ofstream out(output);
    out << "organization,own_score,reference_score,gap,benchmark_pressure,investment_response,reputation_anxiety\n";

    for (int i = 1; i <= n; ++i) {
        double own = 40.0 + 30.0 * uniform(rng);
        double ref = 40.0 + 30.0 * uniform(rng);
        double gap = own - ref;
        double pressure = gap < 0.0 ? -gap : 0.25 * gap;
        double investment = std::max(0.0, 4.0 + 0.35 * pressure + noise(rng));
        double anxiety = std::max(0.0, 3.0 + 0.30 * pressure + noise(rng));

        out << i << "," << own << "," << ref << "," << gap << "," << pressure << "," << investment << "," << anxiety << "\n";
    }

    std::cout << "Wrote organizational benchmarking simulation to: " << output << "\n";
    return 0;
}
