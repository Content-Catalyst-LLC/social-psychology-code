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

    double internal_success_sum = 0.0;
    double internal_failure_sum = 0.0;
    double external_success_sum = 0.0;
    double external_failure_sum = 0.0;
    int success_n = 0;
    int failure_n = 0;

    for (int i = 0; i < n; i++) {
        int success = uniform01() < 0.5 ? 1 : 0;
        double ego_threat = uniform_range(0.0, 10.0);
        double accountability = uniform_range(0.0, 10.0);
        double evidence = uniform_range(0.0, 10.0);

        double internal_attr = 5.0 + 1.5 * success - 1.2 * (1 - success)
            + 0.25 * ego_threat * (2 * success - 1) - 0.20 * accountability + 0.15 * evidence;
        double external_attr = 5.0 - 1.0 * success + 1.5 * (1 - success)
            + 0.25 * ego_threat * (1 - success) - 0.25 * accountability + 0.10 * evidence;

        if (internal_attr < 0.0) internal_attr = 0.0;
        if (internal_attr > 10.0) internal_attr = 10.0;
        if (external_attr < 0.0) external_attr = 0.0;
        if (external_attr > 10.0) external_attr = 10.0;

        if (success) {
            internal_success_sum += internal_attr;
            external_success_sum += external_attr;
            success_n++;
        } else {
            internal_failure_sum += internal_attr;
            external_failure_sum += external_attr;
            failure_n++;
        }
    }

    double ssb = (internal_success_sum / success_n - internal_failure_sum / failure_n)
        + (external_failure_sum / failure_n - external_success_sum / success_n);

    printf("Trials: %d\n", n);
    printf("Mean internal attribution after success: %.3f\n", internal_success_sum / success_n);
    printf("Mean internal attribution after failure: %.3f\n", internal_failure_sum / failure_n);
    printf("Mean external attribution after success: %.3f\n", external_success_sum / success_n);
    printf("Mean external attribution after failure: %.3f\n", external_failure_sum / failure_n);
    printf("Full self-serving bias score: %.3f\n", ssb);
    return 0;
}
