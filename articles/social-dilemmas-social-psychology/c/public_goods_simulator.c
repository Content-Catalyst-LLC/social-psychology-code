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

    double contribution_sum = 0.0;
    double free_ride_sum = 0.0;

    for (int i = 0; i < n; i++) {
        double endowment = 20.0;
        double trust = 10.0 * uniform01();
        double norm = 10.0 * uniform01();
        double enforcement = 10.0 * uniform01();
        double legitimacy = 10.0 * uniform01();
        double reciprocity = 10.0 * uniform01();

        double p = logistic(-2.0 + 0.25 * trust + 0.24 * norm + 0.17 * enforcement + 0.22 * legitimacy + 0.18 * reciprocity);
        double contribution = endowment * p;
        contribution_sum += contribution;
        free_ride_sum += (endowment - contribution) / endowment;
    }

    printf("Trials: %d\n", n);
    printf("Mean contribution: %.3f\n", contribution_sum / n);
    printf("Mean free-riding index: %.3f\n", free_ride_sum / n);
    return 0;
}
