#include <stdio.h>
#include <stdlib.h>

// A messy way of defining generic structs and constructors in C.

// Define a two-element tuple over the generic type T.
#define Tuple2(T) struct { T e1; T e2; }

// Define a constructor for two-element tuples over the generic type T.
// There are some "syntatic errors" here that are fixed when used in the
// example below. I'm making this even more weird.
#define InitTuple2(T, pointer, _1, _2) \
    pointer = malloc(sizeof(Tuple2(T))); \
    if (pointer) { pointer->e1 = _1; pointer->e2 = _2; }

int main() {
    Tuple2(int) *my_tuple;
    InitTuple2(int, my_tuple, 1, 2);
    printf("Hello, World! (%d, %d)\n", my_tuple->e1, my_tuple->e2);
}
