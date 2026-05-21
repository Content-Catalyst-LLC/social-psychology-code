#include <stdio.h>

int main(void) {
    printf("perceived_choice,public_commitment,identity_threat,self_affirmation,spreading_of_alternatives\n");

    for (int choice = 0; choice <= 10; choice++) {
        for (int public_commitment = 0; public_commitment <= 10; public_commitment += 2) {
            for (int threat = 0; threat <= 10; threat += 2) {
                for (int affirmation = 0; affirmation <= 10; affirmation += 2) {
                    double spread = 0.9*choice + 0.7*public_commitment + 0.6*threat - 0.8*affirmation;
                    printf("%d,%d,%d,%d,%.3f\n", choice, public_commitment, threat, affirmation, spread);
                }
            }
        }
    }

    return 0;
}
