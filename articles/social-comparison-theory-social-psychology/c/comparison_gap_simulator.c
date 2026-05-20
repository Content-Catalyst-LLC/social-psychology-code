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

    double eval_change_sum = 0.0;
    double motivation_sum = 0.0;
    double upward_n = 0.0;
    double downward_n = 0.0;

    for (int i = 0; i < n; i++) {
        double self = uniform_range(0.0, 10.0);
        int upward = uniform01() < 0.55 ? 1 : 0;
        double reference = upward ? self + uniform_range(0.0, 4.5) : self - uniform_range(0.0, 4.5);
        if (reference < 0.0) reference = 0.0;
        if (reference > 10.0) reference = 10.0;

        double gap = self - reference;
        double attainability = uniform_range(0.0, 10.0);
        double identity = uniform_range(0.0, 10.0);
        double upward_pressure = gap < 0.0 ? -gap : 0.0;
        double downward_reassurance = gap > 0.0 ? gap : 0.0;

        double eval_change = -0.18 * upward_pressure * identity / 10.0 + 0.15 * downward_reassurance + 0.07 * attainability;
        double motivation = 4.0 + 0.25 * upward_pressure + 0.22 * attainability - 0.20 * upward_pressure * (10.0 - attainability) / 10.0;

        eval_change_sum += eval_change;
        motivation_sum += motivation;
        if (upward) upward_n += 1.0; else downward_n += 1.0;
    }

    printf("Trials: %d\n", n);
    printf("Upward trials: %.0f\n", upward_n);
    printf("Downward trials: %.0f\n", downward_n);
    printf("Mean self-evaluation change: %.3f\n", eval_change_sum / n);
    printf("Mean motivation: %.3f\n", motivation_sum / n);
    return 0;
}
