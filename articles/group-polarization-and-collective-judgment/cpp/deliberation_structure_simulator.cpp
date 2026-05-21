#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_deliberation_structure_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::vector<std::string> conditions = {"unstructured_homogeneous", "devils_advocacy", "minority_protection", "structured_evidence_review"};

    std::ofstream out(output);
    out << "condition,homogeneity,dissent_quality,minority_protection,deliberation_structure,extremity_shift,decision_quality\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double homogeneity = condition == "unstructured_homogeneous" ? 8.5 : condition == "devils_advocacy" ? 5.0 : condition == "minority_protection" ? 4.5 : 3.5;
            double dissent = condition == "unstructured_homogeneous" ? 1.5 : condition == "devils_advocacy" ? 7.0 : condition == "minority_protection" ? 8.0 : 8.5;
            double protection = condition == "minority_protection" ? 8.8 : condition == "structured_evidence_review" ? 8.0 : condition == "devils_advocacy" ? 6.5 : 1.5;
            double structure = condition == "structured_evidence_review" ? 9.0 : condition == "devils_advocacy" ? 7.2 : condition == "minority_protection" ? 7.5 : 2.0;

            homogeneity = std::clamp(homogeneity + noise(rng), 0.0, 10.0);
            dissent = std::clamp(dissent + noise(rng), 0.0, 10.0);
            protection = std::clamp(protection + noise(rng), 0.0, 10.0);
            structure = std::clamp(structure + noise(rng), 0.0, 10.0);

            double extremity = std::clamp(2.0*homogeneity - 1.6*dissent - 1.4*protection - 1.5*structure + noise(rng)*3.0, -30.0, 50.0);
            double quality = std::clamp(50.0 + 3.0*dissent + 2.8*protection + 3.0*structure - 2.2*homogeneity - 0.5*std::max(0.0, extremity) + noise(rng)*6.0, 0.0, 100.0);

            out << condition << "," << homogeneity << "," << dissent << "," << protection << "," << structure << "," << extremity << "," << quality << "\n";
        }
    }

    std::cout << "Wrote deliberation-structure simulation to: " << output << "\n";
    return 0;
}
