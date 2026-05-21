#include <stdio.h>

int main(void) {
    printf("anchor,true_value,adjustment_rate,estimate,anchoring_error\n");

    for (int anchor = 0; anchor <= 100; anchor += 10) {
        for (int true_value = 20; true_value <= 80; true_value += 20) {
            for (int adjustment = 1; adjustment <= 9; adjustment += 2) {
                double rate = adjustment / 10.0;
                double estimate = anchor + rate * (true_value - anchor);
                double error = estimate - true_value;
                printf("%d,%d,%.2f,%.3f,%.3f\n", anchor, true_value, rate, estimate, error);
            }
        }
    }

    return 0;
}
