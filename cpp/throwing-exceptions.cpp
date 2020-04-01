#include <stdexcept>

// Just trying to throw a simple exception.

void throw_exception() {
    throw std::out_of_range("Muh.");
}

int main() {
    throw_exception();
}
