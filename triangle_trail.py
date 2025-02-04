# I don't quite remember what I was trying to do here, honestly. I think drawing an afterimage polygon?
#
# This piece of code is at least a year old (as of 2024) lol

from __future__ import annotations
import itertools
from dataclasses import dataclass
from typing import Optional, Iterable
from math import sqrt, atan2, sin, cos, pi
from collections import deque
import pygame

SCREEN_SIZE = (800, 600)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
MAX_DEQUE_SIZE = 50
WIDTH = 15
FRAMERATE = 60

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main")
    clock = pygame.time.Clock()

    pos_deque = deque[Vector2]()

    is_running = True
    while is_running:
        screen.fill(COLOR_BLACK)

        (mx, my) = pygame.mouse.get_pos()
        pos_deque.appendleft(Vector2(mx, my))

        if len(pos_deque) > MAX_DEQUE_SIZE:
            pos_deque.pop()

        starting_vertex = None
        side_a = []
        side_b = []

        if len(pos_deque) > 1:
            starting_vertex = pos_deque[0]
            prev_v = starting_vertex

            for v in skip(pos_deque, 1):
                diff = v - prev_v
                perp = Vector2(diff.y, -diff.x).normalized()
                side_a.append(v + perp * WIDTH)
                side_b.append(v - perp * WIDTH)
                prev_v = v

        if starting_vertex is not None:
            vertices = (starting_vertex, *side_a, *side_b[::-1])
            as_tuples = [(v.x, v.y) for v in vertices]

            if len(vertices) > 2:
                pygame.draw.polygon(screen, COLOR_WHITE, as_tuples)

            # for (i, v) in enumerate(as_tuples):
            #     pygame.draw.circle(screen, COLOR_GREEN if (i == len(as_tuples) - 1) else COLOR_RED, v, 5.0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        pygame.display.flip()
        clock.tick(FRAMERATE)

@dataclass
class Vector2:
    x: float
    y: float

    def magnitude(self) -> float:
        return sqrt(self.x * self.x + self.y * self.y)

    def normalized(self) -> Vector2:
        mag = self.magnitude()
        if mag == 0:
            return Vector2(0, 0)
        else:
            return self / mag

    def __truediv__(self, rhs: float) -> Vector2:
        return Vector2(self.x / rhs, self.y / rhs)

    def __mul__(self, rhs: float) -> Vector2:
        return Vector2(self.x * rhs, self.y * rhs)

    def __add__(self, rhs: Vector2) -> Vector2:
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs: Vector2) -> Vector2:
        return Vector2(self.x - rhs.x, self.y - rhs.y)

def skip(it: Iterable, n: int) -> Iterable:
    ret = iter(it)
    for _ in range(n):
        next(ret)
    return ret

if __name__ == "__main__":
    main()
