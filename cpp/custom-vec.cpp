#include <iostream>
#include <stdlib.h>

using std::cout;

// TODO: actually make Option<T> and Vec<T>.get() to work.
// TODO: make exceptions work or something.

template <typename T>
class Option {
    private:
        T _content;
    public:
        Option(T t_content) {
            _content = t_content;
        }
        T unwrap();
        bool is_ok();
};

template <typename T>
class Vec {
    private:
        T *_buffer = NULL;
        size_t _len;
    public:
        Vec() {
            _len = 0;
        }
        bool push(T t_item);
        T pop();
        Option<T> get(size_t t_index);
        size_t len();
        T& operator[](size_t t_index);
};

int main() {
    Vec<int> some_vec;
    cout << "Vec length: " << some_vec.len() << "\n";
    cout << "Pushing: " << 10 << "\n";
    some_vec.push(10);
    cout << "Vec length: " << some_vec.len() << "\n";
    cout << "Vec[0]: " << some_vec[0] << "\n";
    cout << "Vec pop: " << some_vec.pop() << "\n";
    return 0;
}

template <typename T>
bool Vec<T>::push(T t_item) {
    T *new_buffer = (T*) realloc(_buffer, (_len + 1) * sizeof(T));
    if (new_buffer == NULL) {
        return false;
    } else {
        _buffer = new_buffer;
        _buffer[_len++] = t_item;
        return true;
    }
}

template <typename T>
T Vec<T>::pop() {
    return (_len == 0)
        ? (T) NULL // Idk if this part makes sense
        : _buffer[--_len];
}

template <typename T>
size_t Vec<T>::len() {
    return _len;
}

template <typename T>
T &Vec<T>::operator[](size_t t_index) {
    if (t_index < 0 || t_index >= _len)
        throw("index out of bounds");
    return _buffer[t_index];
}

template <typename T>
T Option<T>::unwrap() {
    if (_content == NULL)
        throw("option is NULL, failed to unwrap");
    else
        return _content;
}

template <typename T>
bool Option<T>::is_ok() {
    return (_content != NULL);
}

template <typename T>
Option<T> Vec<T>::get(size_t t_index) {
    return (t_index < 0 || t_index >= _len)
        ? new Option<T>(NULL)
        : new Option<T>(_buffer[t_index]);
}

