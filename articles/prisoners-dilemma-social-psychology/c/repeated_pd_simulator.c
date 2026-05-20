#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double uniform01(void) { return (double) rand() / (double) RAND_MAX; }
static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(int argc, char **argv) {
    int n = 10000;
    if (argc > 1) n = atoi(argv[1]);
    srand((unsigned int) time(NULL));

    double cooperation_sum = 0.0;
    double payoff_sum = 0.0;

    for (int i = 0; i < n; i++) {
        double trust = 10.0 * uniform01();
        double expected_partner = 10.0 * uniform01();
        double reputation = 10.0 * uniform01();
        double enforcement = 10.0 * uniform01();
        double temptation_gap = 2.0 - 0.25 * enforcement;

        double p = logistic(-3.0 + 0.35 * trust + 0.30 * expected_partner + 0.18 * reputation + 0.16 * enforcement - 0.55 * temptation_gap);
        int cooperate = uniform01() < p ? 1 : 0;
        int partner = uniform01() < p ? 1 : 0;

        double payoff;
        if (cooperate && partner) payoff = 3.0;
        else if (cooperate && !partner) payoff = 0.0;
        else if (!cooperate && partner) payoff = 5.0 - 0.25 * enforcement;
        else payoff = 1.0;

        cooperation_sum += cooperate;
        payoff_sum += payoff;
    }

    printf("Trials: %d\n", n);
    printf("Mean cooperation rate: %.3f\n", cooperation_sum / n);
    printf("Mean payoff: %.3f\n", payoff_sum / n);
    return 0;
}
