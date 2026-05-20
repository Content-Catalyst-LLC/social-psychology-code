#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

double payoff(int a, int b) {
    if (a == 1 && b == 1) return 3.0;
    if (a == 1 && b == 0) return 0.0;
    if (a == 0 && b == 1) return 5.0;
    return 1.0;
}

int choose(const std::string &strategy, const std::vector<int> &own, const std::vector<int> &opp, std::mt19937 &rng) {
    std::uniform_real_distribution<double> uniform(0.0, 1.0);

    if (strategy == "always_cooperate") return 1;
    if (strategy == "always_defect") return 0;
    if (strategy == "tit_for_tat") return opp.empty() ? 1 : opp.back();
    if (strategy == "generous_tit_for_tat") {
        if (opp.empty()) return 1;
        if (opp.back() == 0 && uniform(rng) < 0.15) return 1;
        return opp.back();
    }
    if (strategy == "win_stay_lose_shift") {
        if (own.empty()) return 1;
        double last = payoff(own.back(), opp.back());
        return last >= 3.0 ? own.back() : 1 - own.back();
    }
    return 0;
}

int main(int argc, char **argv) {
    std::string output = "../outputs/cpp_strategy_tournament.csv";
    if (argc > 1) output = argv[1];

    std::vector<std::string> strategies = {
        "always_cooperate", "always_defect", "tit_for_tat",
        "generous_tit_for_tat", "win_stay_lose_shift"
    };

    const int rounds = 200;
    std::mt19937 rng(42);
    std::ofstream out(output);

    out << "strategy_a,strategy_b,round,choice_a,choice_b,payoff_a,payoff_b,cumulative_a,cumulative_b\n";

    for (const auto &s1 : strategies) {
        for (const auto &s2 : strategies) {
            std::vector<int> h1, h2;
            double score1 = 0.0;
            double score2 = 0.0;

            for (int r = 1; r <= rounds; ++r) {
                int c1 = choose(s1, h1, h2, rng);
                int c2 = choose(s2, h2, h1, rng);
                double p1 = payoff(c1, c2);
                double p2 = payoff(c2, c1);
                score1 += p1;
                score2 += p2;
                h1.push_back(c1);
                h2.push_back(c2);

                out << s1 << "," << s2 << "," << r << "," << c1 << "," << c2 << ","
                    << p1 << "," << p2 << "," << score1 << "," << score2 << "\n";
            }
        }
    }

    std::cout << "Wrote strategy tournament to: " << output << "\n";
    return 0;
}
