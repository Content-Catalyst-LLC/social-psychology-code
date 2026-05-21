#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_institutional_bias_simulation.csv";
    if (argc > 1) output = argv[1];

    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 0.05);
    std::vector<std::string> scenarios = {
        "unstructured_judgment",
        "high_accountability",
        "calibration_feedback",
        "base_rate_prompting",
        "structured_decision_protocol"
    };

    std::ofstream out(output);
    out << "scenario,step,decision_error,accumulated_error,decision_quality\n";

    for (const auto &scenario : scenarios) {
        double accumulated = 0.0;
        double calibration = 0.25;

        for (int step = 1; step <= 120; ++step) {
            double pressure = 0.85;
            double discipline = 0.15;

            if (scenario == "high_accountability") { pressure = 0.55; discipline = 0.65; }
            if (scenario == "calibration_feedback") { pressure = 0.50; discipline = 0.75; }
            if (scenario == "base_rate_prompting") { pressure = 0.45; discipline = 0.80; }
            if (scenario == "structured_decision_protocol") { pressure = 0.35; discipline = 0.90; }

            double error = 0.02 + 0.10*pressure - 0.08*discipline + noise(rng);
            accumulated += error;
            calibration = std::clamp(calibration + 0.04*pressure - 0.05*discipline + noise(rng)/5.0, 0.0, 1.0);
            double quality = std::clamp(1.0 - std::abs(error) - calibration/2.0 + 0.25*discipline, 0.0, 1.0);

            if (step % 2 == 0) {
                out << scenario << "," << step << "," << error << "," << accumulated << "," << quality << "\n";
            }
        }
    }

    std::cout << "Wrote institutional bias simulation to: " << output << "\n";
    return 0;
}
