#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

double logistic(double x) {
    return 1.0 / (1.0 + std::exp(-x));
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_policy_rationalization_simulation.csv";
    if (argc > 1) output = argv[1];

    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 0.03);
    std::vector<std::string> scenarios = {
        "low_sunk_cost_high_accountability",
        "high_sunk_cost_low_accountability",
        "public_commitment_high_identity_threat",
        "evidence_review_with_oversight",
        "face_saving_reversal_pathway"
    };

    std::ofstream out(output);
    out << "scenario,step,commitment_escalation,reversal_probability\n";

    for (const auto &scenario : scenarios) {
        double commitment = 0.45;

        for (int step = 1; step <= 120; ++step) {
            double sunk = 0.5, public_commitment = 0.5, threat = 0.5, evidence = 0.7, accountability = 0.5;

            if (scenario == "low_sunk_cost_high_accountability") {
                sunk = 0.2; public_commitment = 0.2; threat = 0.2; evidence = 0.8; accountability = 0.9;
            } else if (scenario == "high_sunk_cost_low_accountability") {
                sunk = 0.9; public_commitment = 0.8; threat = 0.7; evidence = 0.8; accountability = 0.2;
            } else if (scenario == "public_commitment_high_identity_threat") {
                sunk = 0.7; public_commitment = 0.95; threat = 0.95; evidence = 0.8; accountability = 0.3;
            } else if (scenario == "evidence_review_with_oversight") {
                sunk = 0.5; public_commitment = 0.5; threat = 0.4; evidence = 0.9; accountability = 0.9;
            } else {
                sunk = 0.7; public_commitment = 0.8; threat = 0.8; evidence = 0.8; accountability = 0.7;
            }

            double rationalization = sunk + public_commitment + threat - evidence - accountability;
            commitment += 0.06 * rationalization + noise(rng);
            commitment = std::clamp(commitment, 0.0, 1.0);
            double reversal_probability = logistic(-4.0 * (commitment - 0.5));

            if (step % 2 == 0) {
                out << scenario << "," << step << "," << commitment << "," << reversal_probability << "\n";
            }
        }
    }

    std::cout << "Wrote policy rationalization simulation to: " << output << "\n";
    return 0;
}
