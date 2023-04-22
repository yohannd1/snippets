from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Point2:
    x: float
    y: float

    def __truediv__(self, rhs):
        if isinstance(rhs, Point2):
            return Point2(
                self.x / rhs.x,
                self.y / rhs.y,
            )
        elif isinstance(rhs, (int, float)):
            return Point2(
                self.x / rhs,
                self.y / rhs,
            )
        else:
            raise ValueError(f"Don't know how to divide Point2({type(self.x)}, {type(self.y)}) by {type(rhs)}")

    def __add__(self, rhs):
        if isinstance(rhs, Point2):
            return Point2(
                self.x + rhs.x,
                self.y + rhs.y,
            )
        elif isinstance(rhs, (int, float)):
            return Point2(
                self.x + rhs,
                self.y + rhs,
            )
        else:
            raise ValueError(f"Don't know how to add Point2({type(self.x)}, {type(self.y)}) with {type(rhs)}")

    def copy(self) -> Point2:
        try:
            new_x = self.x.copy()
        except AttributeError:
            new_x = self.x

        try:
            new_y = self.y.copy()
        except AttributeError:
            new_y = self.y

        return Point2(
            new_x,
            new_y,
        )

    def to_tup(self):
        return (self.x, self.y)

