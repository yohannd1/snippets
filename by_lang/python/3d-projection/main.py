from __future__ import annotations

import pygame
import time
import random
import math
import abc

from math import cos, sin, radians, atan2
from typing import Tuple, Optional
from dataclasses import dataclass
from pygame.locals import *

from point import Point2

SCREEN_SIZE = Point2(1200, 700)
SCREEN_CENTER = SCREEN_SIZE / 2

FRAMERATE = 60
SECONDS_PER_FRAME = 1.0 / FRAMERATE

@dataclass
class Color: # FIXME: this is trash
    r: int
    g: int
    b: int

    def to_tup(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)

WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)

def main():
    canvas = PygameCanvas(
        surface=pygame.display.set_mode(SCREEN_SIZE.to_tup())
    )

    global_timer = 0
    bullets = []
    I = 0

    running = True
    while running:
        global_angle = radians(global_timer)

        frame_start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_f:
                    I = max(0, I + 1)
                elif event.key == K_d:
                    I = max(0, I - 1)

        canvas.fill(BLACK)

        base_viewpoint_angle = radians(2 * global_timer)

        AMOUNT_OF_LINES = 20
        for line_i in range(AMOUNT_OF_LINES):
            DIVISION = 50
            MAX_CURVE_SIZE = 250
            for i in range(DIVISION):
                vertical_pos = (SCREEN_SIZE.y / DIVISION) * i
                curvature_distance = MAX_CURVE_SIZE * cos(radians(180 * vertical_pos / SCREEN_SIZE.y))
                viewpoint_angle = base_viewpoint_angle + radians(line_i * 360 / AMOUNT_OF_LINES)

                col = 127.5 + sin(viewpoint_angle) * 127.5 / 2

                OscillatingSpeedBullet(
                    position=Point2(SCREEN_CENTER.x + cos(viewpoint_angle) * curvature_distance, vertical_pos),
                    size=Point2(5, 5),
                    speed_minmax=(0, 0),
                    angle=0,
                    timer_inc=0,
                    color=Color(col, col, col),
                ).draw_to(canvas)

        canvas.update()

        elapsed = time.time() - frame_start
        time.sleep(max(0, SECONDS_PER_FRAME - elapsed))

        global_timer += 1

    pygame.quit()

@dataclass
class Canvas:
    @abc.abstractmethod
    def fill(self, color: Color): ...

    @abc.abstractmethod
    def draw_rect(self, top_left: Point2, size: Point2, color: Color): ...

    @abc.abstractmethod
    def update(self): ...

    def draw_rect_centered(self, center: Point2, size: Point2, color: Color):
        pos = Point2(
            x = center.x - size.x / 2,
            y = center.y - size.y / 2,
        )

        self.draw_rect(pos, size, color)

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
        return self.is_out_of_screen(SCREEN_SIZE) # FIXME: haha global variable

    def is_out_of_screen(self, screen_dimensions: Point2) -> bool:
        pos = self.position
        size = self.size
        scr = screen_dimensions

        return (
            pos.x + size.x < 0 or
            scr.x < pos.x or
            pos.y + size.y < 0 or
            scr.y < pos.y
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
            raise ValueError(f"Minimal value {mn} (first) should be smaller or equal to maximum value {mx} (second)")

    def should_delete(self) -> bool:
        return self.is_out_of_screen(SCREEN_SIZE)

    def is_out_of_screen(self, screen_dimensions: Point2) -> bool:
        pos = self.position
        size = self.size
        scr = screen_dimensions

        return (
            pos.x + size.x < 0 or
            scr.x < pos.x or
            pos.y + size.y < 0 or
            scr.y < pos.y
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
        canvas.draw_rect_centered(self.position, self.size, self.color or Color(150, 180, 120))

if __name__ == "__main__":
    main()
