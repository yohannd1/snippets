from __future__ import annotations

import pygame
import time
import math
import abc
from random import random
from math import cos, sin, radians, atan2
from typing import Tuple, Optional, Sequence, Callable
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
            raise ValueError(
                f"Don't know how to divide Point2({type(self.x)}, {type(self.y)}) by {type(rhs)}"
            )

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
            raise ValueError(
                f"Don't know how to add Point2({type(self.x)}, {type(self.y)}) with {type(rhs)}"
            )

    def copy(self) -> Point2:
        return Point2(self.x, self.y)

    def to_tup(self):
        return (self.x, self.y)


@dataclass
class Color:
    r: int
    g: int
    b: int

    def to_tup(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)


SCREEN_SIZE = Point2(1200, 700)  # o tamanho da tela
SCREEN_CENTER = SCREEN_SIZE / 2  # coordenadas do meio da tela

FRAMERATE = 20  # taxa de atualização (Hz)
FRAME_PERIOD = 1.0 / FRAMERATE  # período de um frame (sec)

BG_COLOR = Color(30, 30, 25)
LINE_COLOR = Color(128, 128, 128)
INDIV_COLOR = Color(255, 0, 0)
TEXT_COLOR = Color(200, 200, 200)

POPL_SIZE = 100  # tamanho da população
X_INTERVAL = (0, 50)  # intervalo de busca do mínimo

# função de busca
FUNCTION = lambda x: 0.02 * x**2 - 0.8 * x + cos(x) + 10


def main() -> None:
    pygame.font.init()
    canvas = PygameCanvas(surface=pygame.display.set_mode(SCREEN_SIZE.to_tup()))

    mf = MinimumFinder()

    running = True
    while running:
        frame_start = time.time()
        next_generation = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == ord("n"):
                    next_generation = True

        mf.process()

        canvas.fill(BG_COLOR)
        mf.draw_to(canvas)

        canvas.update()

        # isso aqui é necessário para garantir a taxa de atualização correta
        elapsed = time.time() - frame_start
        time.sleep(max(0, FRAME_PERIOD - elapsed))

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

    def fill(self, color: Color) -> None:
        self.surface.fill((color.r, color.g, color.b))

    def draw_rect(self, top_left: Point2, size: Point2, color: Color) -> None:
        pygame.draw.rect(
            self.surface,
            (color.r, color.g, color.b),
            pygame.Rect(
                top_left.to_tup(),
                size.to_tup(),
            ),
        )

    def draw_line(
        self, start: Point2, end: Point2, thickness: float, color: Color
    ) -> None:
        pygame.draw.line(
            self.surface,
            (color.r, color.g, color.b),
            start.to_tup(),
            end.to_tup(),
            int(thickness),
        )

    def draw_surface(self, surface: pygame.Surface, pos: Point2) -> None:
        self.surface.blit(surface, pos.to_tup())

    def update(self) -> None:
        pygame.display.update()


@dataclass
class BaseEntity:
    position: Point2

    @abc.abstractmethod
    def process(self) -> None: ...

    @abc.abstractmethod
    def draw_to(self, canvas: Canvas) -> None: ...


class MinimumFinder(BaseEntity):
    def __init__(self) -> None:
        xs, ys = MinimumFinder._calc_function_points(
            func=FUNCTION,
            interval=X_INTERVAL,
            n=int(SCREEN_SIZE.x / 3), # escolhendo uma resolução baseada no tamanho da tela
        )

        self.func_xs, self.func_ys = xs, ys

        self.min_x, self.max_x = xs[0], xs[-1]
        self.amp_x = self.max_x - self.min_x

        self.min_y, self.max_y = min(ys), max(ys)
        self.amp_y = self.max_y - self.min_y

        # ampliar um pouco mais o intervalo y para facilitar visualização
        MAGNIFY_RATE = 0.075
        self.min_y -= self.amp_y * MAGNIFY_RATE
        self.max_y += self.amp_y * MAGNIFY_RATE

        # criar a população inicial - ela é um conjunto de pontos x aleatórios
        self.population = [MinimumFinder._make_random_x() for _ in range(POPL_SIZE)]

        self.font = pygame.font.SysFont("Arial", 20)
        self.best: Optional[Point2] = None

    @staticmethod
    def _calc_function_points(
        func: Callable[[float], float],
        interval: tuple[float, float],
        n: int,
    ) -> tuple[list[float], list[float]]:
        """Calcula os pontos da função `func` no intervalo especificado. Retorna xs, ys."""

        x0, xf = interval
        h = (xf - x0) / n
        xs = [x0 + i * h for i in range(n + 1)]
        ys = [func(x) for x in xs]
        return xs, ys

    @staticmethod
    def _make_random_x() -> float:
        """Criar um indivíduo novo aleatório."""
        xmin, xmax = X_INTERVAL
        return xmin + xmax * random()

    def process(self) -> None:
        xs = self.population
        ys = [FUNCTION(x) for x in xs]

        # avaliar cada membro através de um peso (weight), que é só a distância
        # do valor y para o y máximo - quão mais em baixo, maior o peso.
        ws = [self.max_y - y for (x, y) in zip(xs, ys)]

        # criar um novo indivíduo através da média ponderada das posições x e
        # seus pesos
        new_x = sum(x * w for (x, w) in zip(xs, ws)) / sum(ws)
        self.population.append(new_x)

        # adicionar uma mutação à população (novo ponto aleatório)
        self.population.append(MinimumFinder._make_random_x())

        # fazer uma lista ordenada da população, de acordo com seus valores y, e remover o pior
        sorted_by_rank = sorted(zip(xs, ys), key=lambda a: a[1])
        for (x, _) in sorted_by_rank[-2:]:
            self.population.remove(x)

        best_x, best_y = sorted_by_rank[0]
        self.best = Point2(best_x, best_y)

    def draw_to(self, canvas: Canvas) -> None:
        # desenhar gráfico da função (traduzindo coordenadas da função para
        # coordenadas da tela)
        phys_points = [
            Point2(
                (x - self.min_x) / self.amp_x * SCREEN_SIZE.x,
                SCREEN_SIZE.y - (y - self.min_y) / self.amp_y * SCREEN_SIZE.y,
            )
            for (x, y) in zip(self.func_xs, self.func_ys)
        ]
        canvas.draw_lines(phys_points, 2, LINE_COLOR)

        # desenhando pontos da população
        for x in self.population:
            x_phys = (x - self.min_x) / self.amp_x * SCREEN_SIZE.x
            y_phys = SCREEN_SIZE.y - (FUNCTION(x) - self.min_y) / self.amp_y * SCREEN_SIZE.y
            canvas.draw_rect_centered(Point2(x_phys, y_phys), Point2(5, 5), INDIV_COLOR)

        text_surface = self.font.render(f"Mínimo atual: {self.best}", False, TEXT_COLOR.to_tup())
        canvas.draw_surface(text_surface, Point2(0, 0))

if __name__ == "__main__":
    main()
