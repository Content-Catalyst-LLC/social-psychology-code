#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int periods = 60;
    if (argc > 1) periods = atoi(argv[1]);

    double resource = 100.0;
    double capacity = 150.0;
    double regen_rate = 0.12;
    double extraction_per_user = 8.0;
    int users = 6;

    printf("period,resource_stock,regeneration,total_extraction,depletion_risk\n");

    for (int t = 1; t <= periods; t++) {
        double regeneration = regen_rate * resource * (1.0 - resource / capacity);
        if (regeneration < 0.0) regeneration = 0.0;
        double total_extraction = users * extraction_per_user;
        resource = resource + regeneration - total_extraction;
        if (resource < 0.0) resource = 0.0;
        if (resource > capacity) resource = capacity;
        double depletion_risk = 1.0 - resource / capacity;
        printf("%d,%.3f,%.3f,%.3f,%.3f\n", t, resource, regeneration, total_extraction, depletion_risk);
    }

    return 0;
}
