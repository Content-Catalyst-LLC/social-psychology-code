#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(int argc, char **argv) {
    int max_bystanders = 50;
    if (argc > 1) max_bystanders = atoi(argv[1]);

    printf("bystanders,diffusion_responsibility,felt_responsibility,helping_probability\n");

    for (int n = 0; n <= max_bystanders; n++) {
        double diffusion = 1.0 + 1.25 * log(1.0 + n);
        if (diffusion > 10.0) diffusion = 10.0;
        double responsibility = 8.5 - 0.80 * diffusion;
        if (responsibility < 0.0) responsibility = 0.0;
        double probability = logistic(-3.5 + 0.55 * responsibility + 0.35 * 8.0 - 0.40 * diffusion);
        printf("%d,%.3f,%.3f,%.3f\n", n, diffusion, responsibility, probability);
    }

    return 0;
}
