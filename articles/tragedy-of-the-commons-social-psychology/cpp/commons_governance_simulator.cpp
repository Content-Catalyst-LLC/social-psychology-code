#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_commons_governance_simulation.csv";
    if (argc > 1) output = argv[1];

    const int groups = 300;
    const int periods = 60;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::vector<std::string> regimes = {"open_access", "common_property", "state_property", "polycentric"};

    std::vector<double> resource(groups), capacity(groups), regen(groups), legitimacy(groups), monitoring(groups), stewardship(groups);
    std::vector<int> regime_idx(groups);

    for (int i = 0; i < groups; ++i) {
        resource[i] = 80.0 + 50.0 * uniform(rng);
        capacity[i] = 130.0 + 50.0 * uniform(rng);
        regen[i] = 0.08 + 0.08 * uniform(rng);
        regime_idx[i] = (int)(4.0 * uniform(rng));
        if (regimes[regime_idx[i]] == "open_access") {
            legitimacy[i] = 1.0 + 3.0 * uniform(rng);
            monitoring[i] = 0.0 + 3.0 * uniform(rng);
            stewardship[i] = 1.0 + 3.0 * uniform(rng);
        } else {
            legitimacy[i] = 4.0 + 5.0 * uniform(rng);
            monitoring[i] = 3.0 + 6.0 * uniform(rng);
            stewardship[i] = 4.0 + 5.0 * uniform(rng);
        }
    }

    std::ofstream out(output);
    out << "group_id,period,property_regime,resource_stock,mean_extraction,regeneration,legitimacy,monitoring,stewardship,depletion_risk\n";

    for (int t = 1; t <= periods; ++t) {
        for (int i = 0; i < groups; ++i) {
            double extraction = std::clamp(9.0 - 0.28 * legitimacy[i] - 0.25 * monitoring[i] - 0.30 * stewardship[i] + noise(rng), 0.0, 14.0);
            double regrowth = std::max(0.0, regen[i] * resource[i] * (1.0 - resource[i] / capacity[i]));
            resource[i] = std::clamp(resource[i] + regrowth - 6.0 * extraction, 0.0, capacity[i]);
            double depletion_risk = std::clamp(1.0 - resource[i] / capacity[i], 0.0, 1.0);

            out << (i + 1) << "," << t << "," << regimes[regime_idx[i]] << "," << resource[i] << ","
                << extraction << "," << regrowth << "," << legitimacy[i] << "," << monitoring[i] << ","
                << stewardship[i] << "," << depletion_risk << "\n";
        }
    }

    std::cout << "Wrote commons governance simulation to: " << output << "\n";
    return 0;
}
