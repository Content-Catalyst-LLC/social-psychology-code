#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("empathy,cost,recipient_need,helping_probability\n");

    for (int e = 0; e <= 10; e++) {
        for (int c = 0; c <= 10; c++) {
            double need = 7.0;
            double prob = logistic(-4.0 + 0.45 * e + 0.25 * need - 0.40 * c);
            printf("%d,%d,%.1f,%.3f\n", e, c, need, prob);
        }
    }

    return 0;
}
