#include <iostream>
#include <vector>
#include <numeric>

// Toy conformity-pressure example.
// Compile with: g++ cpp/conformity_pressure.cpp -o outputs/conformity_pressure

int main() {
    std::vector<double> peer_signals = {0.8, 0.7, 0.9, 0.6};
    double private_belief = 0.3;
    double conformity_weight = 0.45;

    double peer_mean = std::accumulate(peer_signals.begin(), peer_signals.end(), 0.0) / peer_signals.size();
    double updated = private_belief + conformity_weight * (peer_mean - private_belief);

    std::cout << "Updated belief: " << updated << "\n";
    return 0;
}
