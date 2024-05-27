# Box implementation in python.
# This kind of box is basically a class where a variable is stored
# inside. Any value can be stored in there - be them primitive types or
# any other type of object -, retrieved and changed.

class Box:
    def __init__(self, content=None):
        self._content = content

    def get(self):
        return self._content

    def set(self, new_content):
        self._content = new_content

    def __repr__(self):
        return f"Box({self._content.__repr__()})"

    __str__ = __repr__

if __name__ == "__main__":
    my_box = Box(10)
    print(my_box, "->", my_box.get())
    my_box.set([1, 2])
    print(my_box, "->", my_box.get())
