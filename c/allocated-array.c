#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Hello, World!\n");

    int *array = NULL;
    size_t array_len = 0;

    for (int i = 0; i < 10; i++) {
        array = realloc(array, ++array_len * sizeof(*array));
        if (array == NULL) {
            printf("Allocation error: stack overflow.\n");
            return 127;
        } else {
            array[array_len - 1] = i;
        }
    }

    printf("Last number: %d\n", array[array_len - 1]);

    return 0;
}
