#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double uniform01(void) { return (double) rand() / (double) RAND_MAX; }
static double uniform_range(double min, double max) { return min + (max - min) * uniform01(); }

int main(int argc, char **argv) {
    int n = 10000;
    if (argc > 1) n = atoi(argv[1]);
    srand((unsigned int) time(NULL));

    double fae_sum = 0.0;
    double constraint_neglect_sum = 0.0;

    for (int i = 0; i < n; i++) {
        double actual_constraint = uniform_range(0.0, 10.0);
        double cognitive_load = uniform_range(0.0, 10.0);
        double accountability = uniform_range(0.0, 10.0);
        double perspective = uniform_range(0.0, 10.0);
        double perceived_constraint = actual_constraint - 0.30 * cognitive_load + 0.30 * accountability + 0.25 * perspective;

        if (perceived_constraint < 0.0) perceived_constraint = 0.0;
        if (perceived_constraint > 10.0) perceived_constraint = 10.0;

        double disposition = 5.0 + 0.35 * cognitive_load - 0.30 * perceived_constraint - 0.20 * accountability;
        double situation = 3.0 + 0.50 * perceived_constraint + 0.25 * accountability + 0.25 * perspective - 0.20 * cognitive_load;

        if (disposition < 0.0) disposition = 0.0;
        if (disposition > 10.0) disposition = 10.0;
        if (situation < 0.0) situation = 0.0;
        if (situation > 10.0) situation = 10.0;

        fae_sum += disposition - situation;
        constraint_neglect_sum += actual_constraint - perceived_constraint;
    }

    printf("Trials: %d\n", n);
    printf("Mean FAE score: %.3f\n", fae_sum / n);
    printf("Mean constraint neglect: %.3f\n", constraint_neglect_sum / n);
    return 0;
}
