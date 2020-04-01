#include <iostream>
#include <stdexcept>
#include <stdlib.h>

// Implementation of a dynamic array and some code to test it.

template <typename T>
class DynamicArray {
    private:
        T *_buffer;
        size_t _len;
    public:
        DynamicArray();
        bool push(T t_item);
        T pop();
        size_t len();
        T& operator[](size_t t_index);
        char[] to_string();
};

template <typename T>
DynamicArray<T>::DynamicArray() {
    _len = 0;
}

template <typename T>
bool DynamicArray<T>::push(T t_item) {
    T *new_buffer = (T *) realloc(_buffer, (_len + 1) * sizeof(T));
    if (new_buffer == NULL) {
        return false;
    }
    _buffer = new_buffer;
    _buffer[_len++] = t_item;
    return true;
}

template <typename T>
T DynamicArray<T>::pop() {
    if (_len == 0)
        throw std::out_of_range("Array is empty.");
    return _buffer[--_len];
}

template <typename T>
size_t DynamicArray<T>::len() {
    return _len;
}

template <typename T>
T& DynamicArray<T>::operator[](size_t t_index) {
    if (t_index < 0 || t_index >= _len)
        throw std::out_of_range("Index is out of range.");
    return _buffer[t_index];
}

int main() {
    using std::cout;

    DynamicArray<int> my_array;
    cout << "+ Array length: " << my_array.len() << "\n";
    int item = 10;
    cout << "  Pushing: " << item << "\n";
    my_array.push(item);
    cout << "+ Array length: " << my_array.len() << "\n";
    cout << "  Array[0]: " << my_array[0] << "\n";
    cout << "  Array pop: " << my_array.pop() << "\n";
    cout << "+ Array length: " << my_array.len() << "\n";
}
