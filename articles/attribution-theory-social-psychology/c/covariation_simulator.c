#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("consensus,distinctiveness,consistency,situational_constraint,p_situational_attribution\n");

    for (int consensus = 0; consensus <= 10; consensus += 2) {
        for (int distinctiveness = 0; distinctiveness <= 10; distinctiveness += 2) {
            for (int consistency = 0; consistency <= 10; consistency += 2) {
                for (int constraint = 0; constraint <= 10; constraint += 2) {
                    double latent = -3.0 + 0.25*consensus + 0.30*distinctiveness + 0.25*consistency + 0.35*constraint;
                    printf("%d,%d,%d,%d,%.6f\n", consensus, distinctiveness, consistency, constraint, logistic(latent));
                }
            }
        }
    }

    return 0;
}
