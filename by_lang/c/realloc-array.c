#include <stdio.h>
#include <stdlib.h>

/*
 * A simple demo of utilizing realloc to change the size of an array.
 */

int main() {
    int *array = NULL;
    size_t array_len = 0;

    for (int i = 0; i < 10; i++) {
        array = realloc(array, ++array_len * sizeof(*array));
        if (array == NULL) {
            printf("allocation error\n");
            return 1;
        } else {
            array[array_len - 1] = i * 2;
        }
    }

    printf("last number: %d\n", array[array_len - 1]);

    return 0;
}
