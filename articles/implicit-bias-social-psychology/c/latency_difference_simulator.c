#include <math.h>
#include <stdio.h>

int main(void) {
    printf("cognitive_load,time_pressure,accountability,structured_support,expected_latency_difference_ms\n");

    for (int load = 0; load <= 10; load++) {
        for (int time = 0; time <= 10; time++) {
            for (int accountability = 0; accountability <= 10; accountability += 2) {
                for (int structure = 0; structure <= 10; structure += 2) {
                    double diff = 100.0 + 12.0*load + 10.0*time - 9.0*accountability - 10.0*structure;
                    if (diff < 0) diff = 0;
                    printf("%d,%d,%d,%d,%.3f\n", load, time, accountability, structure, diff);
                }
            }
        }
    }

    return 0;
}
