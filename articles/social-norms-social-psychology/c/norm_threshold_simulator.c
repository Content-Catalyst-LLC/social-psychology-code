#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("perceived_compliance,approval,threshold,tipping_margin,compliance_probability\n");

    for (int compliance = 0; compliance <= 100; compliance += 5) {
        double approval = 70.0;
        double threshold = 55.0;
        double trend = 15.0;
        double tipping_exposure = compliance + 0.45 * trend + 0.20 * approval;
        double tipping_margin = tipping_exposure - threshold;
        double prob = logistic(-3.0 + 0.030 * compliance + 0.030 * approval + 0.020 * trend + 0.035 * tipping_margin);

        printf("%d,%.1f,%.1f,%.3f,%.3f\n", compliance, approval, threshold, tipping_margin, prob);
    }

    return 0;
}
