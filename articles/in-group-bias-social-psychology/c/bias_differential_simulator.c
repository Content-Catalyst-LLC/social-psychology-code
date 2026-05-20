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

    double ingroup_trust_sum = 0.0;
    double outgroup_trust_sum = 0.0;
    double ingroup_alloc_sum = 0.0;
    double outgroup_alloc_sum = 0.0;
    int ingroup_n = 0;
    int outgroup_n = 0;

    for (int i = 0; i < n; i++) {
        int ingroup = uniform01() < 0.5 ? 1 : 0;
        double identity = uniform_range(0.0, 10.0);
        double threat = uniform_range(0.0, 10.0);
        double norm = uniform_range(0.0, 10.0);
        double bias_force = ingroup ? (0.30 * identity + 0.22 * threat + 0.18 * norm) : (-0.10 * threat);
        double trust = fmax(0.0, fmin(10.0, 5.0 + 0.55 * bias_force));
        double allocation = fmax(0.0, fmin(100.0, 50.0 + 4.8 * bias_force));

        if (ingroup) {
            ingroup_trust_sum += trust;
            ingroup_alloc_sum += allocation;
            ingroup_n++;
        } else {
            outgroup_trust_sum += trust;
            outgroup_alloc_sum += allocation;
            outgroup_n++;
        }
    }

    printf("Trials: %d\n", n);
    printf("Mean ingroup trust: %.3f\n", ingroup_trust_sum / ingroup_n);
    printf("Mean outgroup trust: %.3f\n", outgroup_trust_sum / outgroup_n);
    printf("Trust bias differential: %.3f\n", ingroup_trust_sum / ingroup_n - outgroup_trust_sum / outgroup_n);
    printf("Allocation bias differential: %.3f\n", ingroup_alloc_sum / ingroup_n - outgroup_alloc_sum / outgroup_n);
    return 0;
}
