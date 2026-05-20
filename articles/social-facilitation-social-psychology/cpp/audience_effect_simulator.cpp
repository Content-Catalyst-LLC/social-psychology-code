#include <algorithm>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_audience_effect_simulation.csv";
    if (argc > 1) output = argv[1];

    const int cases = 10000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> uniform(0.0, 1.0);
    std::normal_distribution<double> noise(0.0, 5.0);
    std::vector<std::string> conditions = {"alone", "mere_presence", "evaluation", "digital_monitoring"};

    std::ofstream out(output);
    out << "condition,baseline_skill,task_difficulty,task_mastery,dominant_response_correct,social_presence,evaluation_pressure,arousal,performance\n";

    for (const auto &condition : conditions) {
        for (int i = 0; i < cases; ++i) {
            double baseline_skill = 10.0 * uniform(rng);
            double task_difficulty = 10.0 * uniform(rng);
            double task_mastery = std::clamp(baseline_skill - 0.25 * task_difficulty + noise(rng) / 5.0, 0.0, 10.0);
            int dominant_correct = task_mastery >= task_difficulty ? 1 : 0;

            double social_presence = condition == "alone" ? 0.0 : condition == "evaluation" ? 1.4 : condition == "digital_monitoring" ? 1.1 : 1.0;
            double evaluation_pressure = condition == "alone" ? 0.3 : condition == "mere_presence" ? 2.0 : condition == "evaluation" ? 8.0 : 7.0;
            double arousal = std::clamp(2.0 + 0.8 * social_presence + 0.55 * evaluation_pressure, 0.0, 10.0);
            double performance = std::clamp(
                55.0 + 3.0 * baseline_skill + 2.0 * task_mastery - 2.0 * task_difficulty +
                2.0 * arousal * dominant_correct - 2.2 * arousal * (1 - dominant_correct) + noise(rng),
                0.0, 100.0
            );

            out << condition << "," << baseline_skill << "," << task_difficulty << "," << task_mastery << ","
                << dominant_correct << "," << social_presence << "," << evaluation_pressure << ","
                << arousal << "," << performance << "\n";
        }
    }

    std::cout << "Wrote audience-effect simulation to: " << output << "\n";
    return 0;
}
