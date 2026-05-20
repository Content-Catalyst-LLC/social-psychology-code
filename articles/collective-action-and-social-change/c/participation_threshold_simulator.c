#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double uniform01(void) { return (double) rand() / (double) RAND_MAX; }
static double uniform_range(double min, double max) { return min + (max - min) * uniform01(); }
static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(int argc, char **argv) {
    int n = 10000;
    if (argc > 1) n = atoi(argv[1]);
    srand((unsigned int) time(NULL));

    double participation_sum = 0.0;
    double intention_sum = 0.0;
    double cost_sum = 0.0;

    for (int i = 0; i < n; i++) {
        double identity = uniform_range(0.0, 10.0);
        double injustice = uniform_range(0.0, 10.0);
        double efficacy = uniform_range(0.0, 10.0);
        double network = uniform_range(0.0, 10.0);
        double cost = uniform_range(0.0, 10.0);
        double risk = uniform_range(0.0, 10.0);
        double outrage = fmax(0.0, fmin(10.0, 0.55 * injustice + 0.25 * identity + uniform_range(-1.0, 1.0)));
        double propensity = -3.0 + 0.22 * identity + 0.18 * injustice + 0.20 * outrage + 0.21 * efficacy + 0.16 * network - 0.18 * cost - 0.15 * risk;
        double intention = logistic(propensity);
        int participation = uniform01() < intention ? 1 : 0;

        participation_sum += participation;
        intention_sum += intention;
        cost_sum += cost;
    }

    printf("Trials: %d\n", n);
    printf("Participation rate: %.3f\n", participation_sum / n);
    printf("Mean intention: %.3f\n", intention_sum / n);
    printf("Mean cost: %.3f\n", cost_sum / n);
    return 0;
}
