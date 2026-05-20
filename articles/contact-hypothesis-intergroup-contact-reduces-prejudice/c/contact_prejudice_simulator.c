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

    double pre_sum = 0.0;
    double post_sum = 0.0;
    double quality_sum = 0.0;

    for (int i = 0; i < n; i++) {
        double prejudice_pre = uniform_range(3.0, 9.0);
        double contact_quality = uniform_range(0.0, 10.0);
        double allport_quality = uniform_range(0.0, 10.0);
        double negative_contact = uniform_range(0.0, 5.0);
        double anxiety = fmax(0.0, fmin(10.0, 6.0 - 0.25 * contact_quality + 0.35 * negative_contact));
        double empathy = fmax(0.0, fmin(10.0, 4.0 + 0.25 * contact_quality - 0.10 * negative_contact));
        double prejudice_post = fmax(0.0, fmin(10.0, prejudice_pre - 0.16 * contact_quality - 0.08 * allport_quality - 0.10 * empathy + 0.16 * anxiety + 0.22 * negative_contact));

        pre_sum += prejudice_pre;
        post_sum += prejudice_post;
        quality_sum += contact_quality;
    }

    printf("Trials: %d\n", n);
    printf("Mean pre-contact prejudice: %.3f\n", pre_sum / n);
    printf("Mean post-contact prejudice: %.3f\n", post_sum / n);
    printf("Mean contact quality: %.3f\n", quality_sum / n);
    printf("Mean prejudice change: %.3f\n", (post_sum - pre_sum) / n);
    return 0;
}
