#include <math.h>
#include <stdio.h>

int main(void) {
    printf("period,mean_attitude,mean_extremity,homogeneity,norm_enforcement,safeguards\n");

    double attitude = 25.0;
    double homogeneity = 8.0;
    double enforcement = 7.0;
    double safeguards = 3.0;

    for (int t = 1; t <= 20; t++) {
        double direction = attitude >= 0.0 ? 1.0 : -1.0;
        double amplification = 0.65 * homogeneity + 0.55 * enforcement - 0.80 * safeguards;
        attitude += direction * amplification;

        if (attitude > 100.0) attitude = 100.0;
        if (attitude < -100.0) attitude = -100.0;

        printf("%d,%.3f,%.3f,%.3f,%.3f,%.3f\n", t, attitude, fabs(attitude), homogeneity, enforcement, safeguards);
    }

    return 0;
}
