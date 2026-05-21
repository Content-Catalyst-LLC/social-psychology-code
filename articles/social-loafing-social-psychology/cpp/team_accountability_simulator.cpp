#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>
int main(int argc, char **argv) {
    std::string outpath = argc > 1 ? argv[1] : "../outputs/cpp_team_accountability_simulation.csv";
    std::mt19937 rng(42);
    std::normal_distribution<double> noise(0.0, 1.0);
    std::ofstream out(outpath);
    out << "condition,group_size,identifiability,accountability,digital_traceability,motivation_loss,solo_effort,group_effort,effort_loss\n";
    std::vector<std::string> conditions = {"pooled_group","identifiable_group","high_accountability","traceable_digital_team"};
    for (auto &c : conditions) {
        for (int i=0; i<10000; ++i) {
            double n = (c=="pooled_group" || c=="traceable_digital_team") ? 8 : 6;
            double ident = c=="pooled_group" ? 2 : c=="traceable_digital_team" ? 8 : 7;
            double acct = c=="pooled_group" ? 2 : c=="high_accountability" ? 9 : 7.5;
            double trace = c=="traceable_digital_team" ? 9 : c=="pooled_group" ? 0 : 3;
            double mloss = std::clamp(3 + 1.5*std::log1p(n) - .8*ident - .8*acct - .4*trace + noise(rng)*2, 0.0, 40.0);
            double solo = std::clamp(80 + noise(rng)*7, 0.0, 100.0);
            double group = std::clamp(solo - mloss + noise(rng)*3, 0.0, 100.0);
            out << c << "," << n << "," << ident << "," << acct << "," << trace << "," << mloss << "," << solo << "," << group << "," << solo-group << "\n";
        }
    }
    std::cout << "Wrote " << outpath << "\n";
}
