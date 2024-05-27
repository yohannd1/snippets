# A second take on boxes, this time using dataclasses and a map function.

from __future__ import annotations
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class Box(Generic[T]):
    inner: T

    def map(self, func: Callable[[T], U]) -> Box[U]:
        return Box(inner = func(self.inner))

print(
    Box(20)
    .map(lambda x: x ** 2)
    .inner
)
