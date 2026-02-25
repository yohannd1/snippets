from amaranth import Shape, Const, C, signed, unsigned
from amaranth.lib.wiring import In, Out, Component

# Reference: https://amaranth-lang.org/docs/amaranth/v0.5.8/guide.html

# a shape describes a the width and signedness of a data-type
_ = Shape(width=8, signed=False) # this is 8-bit unsigned
assert unsigned(8) == Shape(width=8, signed=False) # alias: "unsigned"
assert signed(3) == Shape(width=3, signed=True)

# Const: simple (compile-time) constant - shape (type) is inferred to have as
# least bits as possible to represent it
assert Const(10).shape().width == 4
assert Const(10).value == 10

assert C(10).value == 10 # shorthand: "C"

# negative constants have `signed` shapes; otherwise, they are `unsigned`
assert Const(0).shape() == unsigned(1)
assert Const(-3).shape() == signed(3)
assert Const(7).shape() == unsigned(3)

# a constant can have its shape specified in the second argument
assert Const(5, signed(8)).shape() == signed(8)
assert Const(5, 8).shape() == unsigned(8) # plain number defaults to unsigned

# the second argument can also be a range - it is half-open, though!
# the range of values it represents is at least [min(r), max(r))
assert Const(0, range(16)).shape() == unsigned(4) # 0 to 15 -- 4 bits is fine
assert Const(0, range(17)).shape() == unsigned(5) # 0 to 16 -- we need 5 bits
# `Const(8, range(8))` throws a warning, complaining that this is probably not what you wanted. But it gives you `Const(0, unsigned(3))`
# `Const(9, range(8))` doesn't seem to mind, and just defaults to `Const(1, unsigned(3))`
