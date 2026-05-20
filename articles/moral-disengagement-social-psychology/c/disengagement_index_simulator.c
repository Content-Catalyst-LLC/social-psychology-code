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

    double md_sum = 0.0;
    double harmful_prob_sum = 0.0;
    double harmful_count = 0.0;

    for (int i = 0; i < n; i++) {
        double md = 0.0;
        for (int j = 0; j < 8; j++) md += uniform_range(0.0, 10.0);
        md /= 8.0;

        double empathy = uniform_range(0.0, 10.0);
        double guilt = uniform_range(0.0, 10.0);
        double visibility = uniform_range(0.0, 10.0);
        double pressure = uniform_range(0.0, 10.0);

        double p = logistic(-4.0 + 0.45 * md + 0.20 * pressure - 0.25 * empathy - 0.20 * guilt - 0.15 * visibility);

        md_sum += md;
        harmful_prob_sum += p;
        if (uniform01() < p) harmful_count += 1.0;
    }

    printf("Trials: %d\n", n);
    printf("Mean moral disengagement index: %.3f\n", md_sum / n);
    printf("Mean harmful decision probability: %.3f\n", harmful_prob_sum / n);
    printf("Observed harmful decision rate: %.3f\n", harmful_count / n);
    return 0;
}
