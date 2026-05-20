#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static double uniform01(void) { return (double) rand() / (double) RAND_MAX; }

int main(int argc, char **argv) {
    int n = 10000;
    if (argc > 1) n = atoi(argv[1]);
    srand((unsigned int) time(NULL));

    double perf_alone = 0.0, perf_audience = 0.0;
    int n_alone = 0, n_audience = 0;

    for (int i = 0; i < n; i++) {
        int audience = (i % 2);
        double baseline_skill = 10.0 * uniform01();
        double task_difficulty = 10.0 * uniform01();
        double task_mastery = baseline_skill - 0.25 * task_difficulty;
        if (task_mastery < 0.0) task_mastery = 0.0;
        if (task_mastery > 10.0) task_mastery = 10.0;

        int dominant_correct = task_mastery >= task_difficulty ? 1 : 0;
        double evaluation_pressure = audience ? 6.0 : 0.5;
        double arousal = 2.0 + 0.8 * audience + 0.55 * evaluation_pressure;
        double performance = 55.0 + 3.0 * baseline_skill + 2.0 * task_mastery - 2.0 * task_difficulty
            + 2.0 * arousal * dominant_correct - 2.2 * arousal * (1 - dominant_correct);

        if (performance < 0.0) performance = 0.0;
        if (performance > 100.0) performance = 100.0;

        if (audience) {
            perf_audience += performance;
            n_audience++;
        } else {
            perf_alone += performance;
            n_alone++;
        }
    }

    printf("Trials: %d\n", n);
    printf("Mean performance alone: %.3f\n", perf_alone / n_alone);
    printf("Mean performance with audience: %.3f\n", perf_audience / n_audience);
    return 0;
}
