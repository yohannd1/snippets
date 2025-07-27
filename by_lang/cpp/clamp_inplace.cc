#include <iostream>

template <typename T>
void clampInplace(T& val, T min, T max) {
    if (val<min) val=min;
    else if (val>max) val=max;
}

int main() {
    int x = 200;
    clampInplace(x, -20, -1);
    std::cout << x << '\n';
}
