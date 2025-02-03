#include <concepts>
#include <iostream>
#include <string>

/**
 * An experiment with type traits.
 */

template <class T>
auto to_string(const T& obj) -> std::string;

template <class Self>
concept ToString = requires(const Self& self) {
    { to_string(self) } ->std::same_as<std::string>;
};

template <>
auto to_string<int>(const int& obj) -> std::string {
    return std::to_string(obj);
}

auto print(const ToString auto& obj) -> void {
    std::cout << to_string(obj) << '\n';
}

int main() {
    print(50);
    print(255);
}
