# A second take on boxes, this time using dataclasses and a map function.

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Box[T]:
    inner: T

    def map[U](self, func: Callable[[T], U]) -> Box[U]:
        return Box(inner=func(self.inner))

print(
    Box(20)
    .map(lambda x: x ** 2)
    .inner
)
