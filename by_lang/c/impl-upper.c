#include <stdio.h>

/*
 * Iterating over an alphabet string, using math to turn lower into
 * uppercase.
 */

int main() {
    char foo[] = "abcdefghklmnopqrstuvwxyz";
    for (char *i = foo; *i; i++) {
        printf("%c -> %c\n", *i, *i - 32);
    }
}
