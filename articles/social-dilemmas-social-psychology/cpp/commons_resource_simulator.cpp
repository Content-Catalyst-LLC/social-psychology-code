#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_commons_simulation.csv";
    if (argc > 1) output = argv[1];

    const int groups = 250;
    const int periods = 50;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);

    std::vector<double> resource(groups), monitoring(groups), legitimacy(groups), sanction(groups), norm(groups);

    for (int i = 0; i < groups; ++i) {
        resource[i] = 70.0 + 50.0 * uniform(rng);
        monitoring[i] = 1.0 + 8.0 * uniform(rng);
        legitimacy[i] = 1.0 + 8.0 * uniform(rng);
        sanction[i] = 8.0 * uniform(rng);
        norm[i] = 1.0 + 8.0 * uniform(rng);
    }

    std::ofstream out(output);
    out << "group_id,period,resource_stock,mean_extraction,monitoring,legitimacy,sanction,norm_salience\n";

    for (int t = 1; t <= periods; ++t) {
        for (int i = 0; i < groups; ++i) {
            double extraction = std::clamp(
                8.5 - 0.25 * monitoring[i] - 0.25 * legitimacy[i] -
                0.25 * sanction[i] - 0.25 * norm[i] + noise(rng),
                0.0, 15.0
            );
            double total_extraction = 6.0 * extraction;
            double regeneration = std::max(0.0, 0.12 * resource[i] * (1.0 - resource[i] / 150.0));
            resource[i] = std::clamp(resource[i] + regeneration - total_extraction, 0.0, 150.0);

            out << (i + 1) << "," << t << "," << resource[i] << "," << extraction << ","
                << monitoring[i] << "," << legitimacy[i] << "," << sanction[i] << "," << norm[i] << "\n";
        }
    }

    std::cout << "Wrote commons simulation to: " << output << "\n";
    return 0;
}
