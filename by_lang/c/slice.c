#include <stdio.h>

/**
 * A crappy implementation of slices in C.
 */

#define InstSlice(T) struct Slice_##T { \
	T *ptr; \
	unsigned int len; \
}

#define Slice(T) struct Slice_##T

InstSlice(char);

int main(void) {
	Slice(char) c = { "foo", 4 };
	Slice(char) d = { "foo", 4 };
}
