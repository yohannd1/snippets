#include <iostream>
#include <stdexcept>
#include <stdlib.h>

using std::cout;

/* An implementation of a type similar to Maybe on Haskell, or Option
   on Rust. */

template <typename T>
class Maybe {
    private:
        T *_content;
    public:
        Maybe(T *t_content);
        T unwrap();
        bool is_ok();
};

template <typename T>
bool Maybe<T>::is_ok() {
    return (_content != NULL);
}

template <typename T>
T Maybe<T>::unwrap() {
    if (_content) {
        return *_content;
    } else {
        throw std::runtime_error("Failed to unwrap a Maybe class.");
    }
}

template <typename T>
Maybe<T>::Maybe(T *t_content) {
    _content = t_content;
}

int main() {
    int my_int = 10;
    Maybe<int> something(&my_int); /* Change this to NULL and it'll say "None" below. */

    if (something.is_ok()) {
        cout << "Something -> " << something.unwrap();
    } else {
        cout << "Something -> None";
    }
}
