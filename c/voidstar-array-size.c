#include <stdio.h> /* printf */
#include <stdlib.h> /* uint */

uint array_len(void *array_start, uint element_size);

int main() {
	int foo[] = {1, 2, 5, 4, 0};
	printf("Array size: %u\n", array_len(foo, sizeof (int)));
}

uint array_len(void *array_start, uint element_size) {
	uint i;
	printf("~\n");
	for (i = 0; *(int *)(array_start + element_size * i); i++);
	return i;
}
