#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_responsibility_simulation.csv";
    if (argc > 1) output = argv[1];

    std::ofstream out(output);
    out << "intentionality,choice,controllability,situational_constraint,responsibility\n";

    for (int intent = 0; intent <= 10; intent += 1) {
        for (int choice = 0; choice <= 10; choice += 2) {
            for (int control = 0; control <= 10; control += 2) {
                for (int constraint = 0; constraint <= 10; constraint += 2) {
                    double responsibility = 10.0 + 4.0*intent + 3.0*choice + 3.0*control - 3.5*constraint;
                    responsibility = std::clamp(responsibility, 0.0, 100.0);
                    out << intent << "," << choice << "," << control << "," << constraint << "," << responsibility << "\n";
                }
            }
        }
    }

    std::cout << "Wrote responsibility simulation to: " << output << "\n";
    return 0;
}
