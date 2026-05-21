#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("unanimity,visible_dissent,ambiguity,conformity_probability\n");

    for (int unanimity = 0; unanimity <= 10; unanimity++) {
        for (int dissent = 0; dissent <= 10; dissent++) {
            for (int ambiguity = 0; ambiguity <= 10; ambiguity++) {
                double latent = -3.0 + 0.42 * unanimity - 0.48 * dissent + 0.28 * ambiguity;
                printf("%d,%d,%d,%.6f\n", unanimity, dissent, ambiguity, logistic(latent));
            }
        }
    }

    return 0;
}
