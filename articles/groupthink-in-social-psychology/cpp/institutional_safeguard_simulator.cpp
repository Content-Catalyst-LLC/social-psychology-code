#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_institutional_safeguard_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::vector<std::string> conditions = {"no_safeguards", "devils_advocate", "outside_experts", "red_team", "subgroup_review"};

    std::ofstream out(output);
    out << "condition,cohesion,directive_leadership,dissent_visibility,outside_information,safeguards,decision_quality,implementation_risk\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double cohesion = 7.5;
            double directive = condition == "no_safeguards" ? 8.0 : 4.0;
            double dissent = condition == "no_safeguards" ? 2.0 : condition == "devils_advocate" ? 7.5 : condition == "red_team" ? 8.5 : 7.0;
            double outside_info = condition == "outside_experts" ? 9.0 : condition == "red_team" ? 8.5 : condition == "subgroup_review" ? 8.0 : 3.0;
            double safeguards = condition == "no_safeguards" ? 2.0 : condition == "devils_advocate" ? 7.0 : condition == "outside_experts" ? 7.8 : condition == "red_team" ? 8.8 : 8.2;

            cohesion = std::clamp(cohesion + noise(rng), 0.0, 10.0);
            directive = std::clamp(directive + noise(rng), 0.0, 10.0);
            dissent = std::clamp(dissent + noise(rng), 0.0, 10.0);
            outside_info = std::clamp(outside_info + noise(rng), 0.0, 10.0);
            safeguards = std::clamp(safeguards + noise(rng), 0.0, 10.0);

            double risk = (cohesion + directive + 7.0 - dissent - outside_info) / 3.0;
            double quality = std::clamp(55.0 - 4.0*risk + 4.0*safeguards + 2.5*dissent + 2.5*outside_info + noise(rng)*7.0, 0.0, 100.0);
            double implrisk = std::clamp(75.0 + 4.0*risk - 3.0*safeguards - 2.0*dissent - 2.0*outside_info + noise(rng)*7.0, 0.0, 100.0);

            out << condition << "," << cohesion << "," << directive << "," << dissent << "," << outside_info << "," << safeguards << "," << quality << "," << implrisk << "\n";
        }
    }

    std::cout << "Wrote institutional safeguard simulation to: " << output << "\n";
    return 0;
}
