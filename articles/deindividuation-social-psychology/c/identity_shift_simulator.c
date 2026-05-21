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

    double lambda_sum = 0.0;
    double norm_congruence_sum = 0.0;

    for (int i = 0; i < n; i++) {
        double anonymity = 10.0 * uniform01();
        double group_identity = 10.0 * uniform01();
        double norm_clarity = 10.0 * uniform01();
        double accountability = 10.0 * uniform01();

        double lambda_group = logistic(-2.0 + 0.32 * anonymity + 0.30 * group_identity + 0.18 * norm_clarity - 0.20 * accountability);
        double norm_congruence = 2.0 + 7.0 * lambda_group;
        if (norm_congruence > 10.0) norm_congruence = 10.0;

        lambda_sum += lambda_group;
        norm_congruence_sum += norm_congruence;
    }

    printf("Trials: %d\n", n);
    printf("Mean group-regulation weight: %.3f\n", lambda_sum / n);
    printf("Mean norm congruence: %.3f\n", norm_congruence_sum / n);
    return 0;
}
