#include <stdexcept>

void throw_exception() {
    throw std::out_of_range("Muh.");
}

int main() {
    throw_exception();
}
