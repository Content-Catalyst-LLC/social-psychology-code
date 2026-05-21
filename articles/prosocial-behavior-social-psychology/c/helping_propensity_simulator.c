#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("empathy,norm_salience,helping_cost,bystanders,helping_probability\n");

    for (int e = 0; e <= 10; e++) {
        for (int c = 0; c <= 10; c++) {
            int bystanders = 3;
            double norms = 6.0;
            double prob = logistic(-4.2 + 0.35 * e + 0.35 * norms - 0.35 * c - 0.30 * log(1.0 + bystanders));
            printf("%d,%.1f,%d,%d,%.3f\n", e, norms, c, bystanders, prob);
        }
    }

    return 0;
}
