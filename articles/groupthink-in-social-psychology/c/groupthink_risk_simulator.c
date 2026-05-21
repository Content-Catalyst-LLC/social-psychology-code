#include <math.h>
#include <stdio.h>

int main(void) {
    printf("cohesion,leadership_directive,insulation,stress,dissent_visibility,outside_information,groupthink_risk\n");

    for (int cohesion = 0; cohesion <= 10; cohesion++) {
        for (int directive = 0; directive <= 10; directive++) {
            double insulation = 7.0;
            double stress = 7.0;
            double dissent = 3.0;
            double outside_info = 3.0;
            double risk = (cohesion + directive + insulation + stress - dissent - outside_info) / 4.0;
            printf("%d,%d,%.1f,%.1f,%.1f,%.1f,%.3f\n", cohesion, directive, insulation, stress, dissent, outside_info, risk);
        }
    }

    return 0;
}
