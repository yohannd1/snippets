from __future__ import annotations

import pygame
import time
import math
import abc
from random import random
from math import cos, sin, radians, atan2
from typing import Tuple, Optional
from dataclasses import dataclass

from pygame.locals import *

from point import Point2

SCREEN_SIZE = Point2(1200, 700)
SCREEN_CENTER = SCREEN_SIZE / 2

FRAMERATE = 75
SECONDS_PER_FRAME = 1.0 / FRAMERATE


@dataclass
class Color:  # FIXME: this is trash
    r: int
    g: int
    b: int

    def to_tup(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)


WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)


def main():
    canvas = PygameCanvas(surface=pygame.display.set_mode(SCREEN_SIZE.to_tup()))

    global_timer = 0
    bullets = []

    def make_func_points(
        func, interval: tuple[float, float], n: int
    ) -> tuple[list[float], list[float]]:
        x0, xf = interval
        h = (xf - x0) / n
        xs = [x0 + i * h for i in range(n + 1)]
        ys = [func(x) for x in xs]
        return xs, ys

    FUNC = lambda x: 0.02 * x**2 - 0.8 * x + cos(x) + 10
    x_intv = (0, 50)
    xs, ys = make_func_points(FUNC, x_intv, int(SCREEN_SIZE.x / 3))

    GEN_SIZE = 100

    generation = [x_intv[0] + x_intv[1] * random() for _ in range(GEN_SIZE)]

    running = True
    while running:
        global_angle = radians(global_timer)
        frame_start = time.time()
        next_generation = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == ord("n"):
                    next_generation = True

        canvas.fill(BLACK)

        COLOR = Color(128, 128, 128)

        min_x, max_x = xs[0], xs[-1]
        amp_x = max_x - min_x

        min_y, max_y = min(ys), max(ys)

        amp_y = max_y - min_y
        min_y -= amp_y * 0.075
        max_y += amp_y * 0.075

        # actual points upon rendering
        phys_points = [
            Point2(
                (x - min_x) / amp_x * SCREEN_SIZE.x,
                SCREEN_SIZE.y - (y - min_y) / amp_y * SCREEN_SIZE.y,
            )
            for (x, y) in zip(xs, ys)
        ]
        canvas.draw_lines(phys_points, 2, COLOR)

        for x in generation:
            x_phys = (x - min_x) / amp_x * SCREEN_SIZE.x
            y_phys = SCREEN_SIZE.y - (FUNC(x) - min_y) / amp_y * SCREEN_SIZE.y
            canvas.draw_rect_centered(
                Point2(x_phys, y_phys), Point2(5, 5), Color(255, 0, 0)
            )

        canvas.update()

        elapsed = time.time() - frame_start
        time.sleep(max(0, SECONDS_PER_FRAME - elapsed))

        global_timer += 1

        if True:
            g_ys = [FUNC(x) for x in generation]
            g_ws = [max_y - FUNC(x) for x in generation]  # weights
            new_child = sum(x * w for (x, w) in zip(generation, g_ws)) / sum(g_ws)
            generation.append(new_child)

            paired = list(zip(generation, g_ys))
            sorted_by_rank = sorted(paired, key=lambda a: a[1])
            generation.remove(sorted_by_rank[-1][0])
            generation.remove(sorted_by_rank[-2][0])

            generation.append(x_intv[0] + x_intv[1] * random())

    pygame.quit()


@dataclass
class Canvas:
    @abc.abstractmethod
    def fill(self, color: Color) -> None: ...

    @abc.abstractmethod
    def draw_rect(self, top_left: Point2, size: Point2, color: Color) -> None: ...

    @abc.abstractmethod
    def draw_line(
        self, start: Point2, end: Point2, thickness: float, color: Color
    ) -> None: ...

    def draw_lines(
        self, lines: Sequence[Point2], thickness: float, color: Color
    ) -> None:
        for p1, p2 in zip(lines, lines[1:]):
            self.draw_line(p1, p2, thickness, color)

    def draw_rect_centered(self, center: Point2, size: Point2, color: Color) -> None:
        pos = Point2(
            x=center.x - size.x / 2,
            y=center.y - size.y / 2,
        )

        self.draw_rect(pos, size, color)

    @abc.abstractmethod
    def update(self) -> None: ...


@dataclass
class PygameCanvas(Canvas):
    surface: pygame.Surface

    def fill(self, color: Color):
        self.surface.fill((color.r, color.g, color.b))

    def draw_rect(self, top_left: Point2, size: Point2, color: Color):
        pygame.draw.rect(
            self.surface,
            (color.r, color.g, color.b),
            pygame.Rect(
                top_left.to_tup(),
                size.to_tup(),
            ),
        )

    def draw_line(self, start: Point2, end: Point2, thickness: float, color: Color):
        pygame.draw.line(
            self.surface,
            (color.r, color.g, color.b),
            start.to_tup(),
            end.to_tup(),
            thickness,
        )

    @abc.abstractmethod
    def update(self):
        pygame.display.update()


@dataclass
class BaseEntity:
    position: Point2

    @abc.abstractmethod
    def should_delete(self) -> bool: ...

    @abc.abstractmethod
    def process(self): ...

    @abc.abstractmethod
    def draw_to(self, canvas: Canvas): ...


@dataclass
class SimpleBullet(BaseEntity):
    speed: Point2
    size: Point2

    def should_delete(self) -> bool:
        return self.is_out_of_screen(SCREEN_SIZE)  # FIXME: haha global variable

    def is_out_of_screen(self, screen_dimensions: Point2) -> bool:
        pos = self.position
        size = self.size
        scr = screen_dimensions

        return (
            pos.x + size.x < 0 or scr.x < pos.x or pos.y + size.y < 0 or scr.y < pos.y
        )

    def process(self):
        self.position += self.speed

    def draw_to(self, canvas: Canvas):
        canvas.draw_rect_centered(self.position, self.size, Color(150, 180, 120))


@dataclass
class OscillatingSpeedBullet(BaseEntity):
    angle: float
    size: Point2
    speed_minmax: Tuple[float, float]
    timer: int = 0
    timer_inc: int = 1
    color: Optional[Color] = None

    def __post_init__(self):
        mn, mx = self.speed_minmax
        if mn > mx:
            raise ValueError(
                f"Minimal value {mn} (first) should be smaller or equal to maximum value {mx} (second)"
            )

    def should_delete(self) -> bool:
        return self.is_out_of_screen(SCREEN_SIZE)

    def is_out_of_screen(self, screen_dimensions: Point2) -> bool:
        pos = self.position
        size = self.size
        scr = screen_dimensions

        return (
            pos.x + size.x < 0 or scr.x < pos.x or pos.y + size.y < 0 or scr.y < pos.y
        )

    def process(self):
        intensity = cos(radians(self.timer))

        mn, mx = self.speed_minmax
        # middle = (mx - mn) / 2
        speed = mn + (mx - mn) * max(0, intensity)

        self.position += Point2(
            speed * cos(self.angle),
            -speed * sin(self.angle),
        )

        self.timer += self.timer_inc

    def draw_to(self, canvas: Canvas):
        canvas.draw_rect_centered(
            self.position, self.size, self.color or Color(150, 180, 120)
        )


if __name__ == "__main__":
    main()
