#include <stdio.h>

/*
 * Simple demo of a long long integer calculator.
 */

#define intcalc(expr) printf("%s = %lld\n", #expr, expr)

int main() {
    intcalc(20 + 3);
}
