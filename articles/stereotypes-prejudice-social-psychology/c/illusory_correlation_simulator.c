#include <stdio.h>

int main(void) {
    printf("group_base_rate,behavior_base_rate,observed_count,expected_count,illusory_correlation_error\n");

    for (int group_rate = 10; group_rate <= 90; group_rate += 10) {
        for (int behavior_rate = 10; behavior_rate <= 90; behavior_rate += 10) {
            double expected = (group_rate / 100.0) * (behavior_rate / 100.0) * 1000.0;
            double salience_boost = (group_rate < 30 && behavior_rate < 30) ? 18.0 : 0.0;
            double observed = expected + salience_boost;
            double error = observed - expected;
            printf("%d,%d,%.3f,%.3f,%.3f\n", group_rate, behavior_rate, observed, expected, error);
        }
    }

    return 0;
}
