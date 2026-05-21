#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("legitimacy,peer_dissent,escalation_step,obedience_probability\n");

    for (int legitimacy = 0; legitimacy <= 10; legitimacy++) {
        for (int dissent = 0; dissent <= 10; dissent++) {
            for (int step = 1; step <= 12; step++) {
                double latent = -2.1 + 0.45 * legitimacy + 0.22 * step - 0.40 * dissent;
                printf("%d,%d,%d,%.6f\n", legitimacy, dissent, step, logistic(latent));
            }
        }
    }

    return 0;
}
