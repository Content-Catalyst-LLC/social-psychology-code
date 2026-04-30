#include <stdio.h>

// Toy attribution weighting model.
// Compile with: cc c/attribution_weighting.c -o outputs/attribution_weighting

double attribution_score(double dispositional, double situational, double w_d, double w_s) {
    return w_d * dispositional + w_s * situational;
}

int main(void) {
    double score = attribution_score(0.8, 0.3, 0.7, 0.3);
    printf("Attribution score: %.3f\n", score);
    return 0;
}
