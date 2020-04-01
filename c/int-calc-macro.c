#include <stdio.h>

#define intcalc(expr) printf("%s = %d\n", #expr, expr)

int main() {
    intcalc(20 + 3);
}
