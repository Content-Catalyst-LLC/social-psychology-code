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

    double responsibility_sum = 0.0;
    double intervention_prob_sum = 0.0;
    double intervention_count = 0.0;

    for (int i = 0; i < n; i++) {
        int bystanders = (int) uniform_range(0.0, 12.0);
        double ambiguity = uniform_range(0.0, 10.0);
        double evaluation = uniform_range(0.0, 10.0);
        double role_clarity = uniform_range(0.0, 10.0);
        double efficacy = uniform_range(0.0, 10.0);
        double concern = uniform_range(0.0, 10.0);

        double responsibility = 7.0 + 0.40 * role_clarity - 0.70 * log1p((double)bystanders) - 0.25 * ambiguity - 0.20 * evaluation;
        if (responsibility < 0.0) responsibility = 0.0;
        if (responsibility > 10.0) responsibility = 10.0;

        double p = logistic(-3.5 + 0.50 * responsibility + 0.25 * role_clarity + 0.25 * efficacy + 0.25 * concern - 0.20 * ambiguity - 0.20 * evaluation);

        responsibility_sum += responsibility;
        intervention_prob_sum += p;
        if (uniform01() < p) intervention_count += 1.0;
    }

    printf("Trials: %d\n", n);
    printf("Mean perceived responsibility: %.3f\n", responsibility_sum / n);
    printf("Mean intervention probability: %.3f\n", intervention_prob_sum / n);
    printf("Observed intervention rate: %.3f\n", intervention_count / n);
    return 0;
}
