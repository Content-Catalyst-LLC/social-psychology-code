#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int max_group = argc > 1 ? atoi(argv[1]) : 12;
    printf("group_size,per_person_effort,total_output,motivation_loss,coordination_loss\n");
    for (int n = 1; n <= max_group; n++) {
        double coord = 2.0 * log(1.0 + n);
        double motiv = 4.0 * log(1.0 + n);
        double effort = 100.0 - coord - motiv;
        if (effort < 0) effort = 0;
        printf("%d,%.3f,%.3f,%.3f,%.3f\n", n, effort, n*effort, motiv, coord);
    }
    return 0;
}
