#include <math.h>
#include <stdio.h>

static double logistic(double x) {
    if (x > 40.0) return 1.0;
    if (x < -40.0) return 0.0;
    return 1.0 / (1.0 + exp(-x));
}

int main(void) {
    printf("resource_competition,identity_salience,symbolic_threat,contact_quality,conflict_intensity\n");

    for (int r = 0; r <= 10; r++) {
        for (int i = 0; i <= 10; i++) {
            double symbolic = 6.0;
            double contact = 3.0;
            double intensity = 100.0 * logistic(-2.0 + 0.35*r + 0.28*i + 0.35*symbolic - 0.35*contact);
            printf("%d,%d,%.1f,%.1f,%.3f\n", r, i, symbolic, contact, intensity);
        }
    }

    return 0;
}
