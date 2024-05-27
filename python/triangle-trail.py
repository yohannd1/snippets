# I don't quite remember what I was trying to do here, honestly. This piece of code is at least a year old (as of 2024) lol

import math, itertools
from typing import Optional
import pygame

# TODO: find out how to make the trail longer (maybe add more )

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main")
    clock = pygame.time.Clock()

    pos_1 = (0, 0)
    pos_queue = Queue(slots=20)

    done = False
    while not done:
        screen.fill((0, 0, 0))

        base_pos = pos_queue.get(pos_queue.read_ptr)
        right_poses = []
        left_poses = []

        i = (pos_queue.read_ptr + 1) % pos_queue.len()
        while i != pos_queue.read_ptr:
            pos_0 = pos_queue.get(i)
            pos_1 = pos_queue.get((i + 1) % pos_queue.len())

            if pos_0 is None or pos_1 is None:
                break

            angle_between = math.atan2(pos_1[1] - pos_0[1], pos_1[0] - pos_0[0])
            cos_fact = math.cos(angle_between + math.radians(90))
            sin_fact = math.sin(angle_between + math.radians(90))

            width = 10 # TODO: make this dynamic, I guess

            right_poses.append((
                (pos_1[0] - width * cos_fact, pos_1[1] - width * sin_fact)
            ))

            left_poses.append((
                (pos_1[0] + width * cos_fact, pos_1[1] + width * sin_fact)
            ))

            i = (i + 1) % pos_queue.len()

            # TODO: figure out why tf the last point is exploding

        assert len(right_poses) == len(left_poses)

        if len(right_poses) > 0:
            pygame.draw.polygon(
                screen,
                (255, 255, 255),
                (base_pos, *right_poses, pygame.mouse.get_pos())
            )

        pos_queue.store(pygame.mouse.get_pos())

        print("X")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        clock.tick(60)
        pygame.display.flip()

class Queue:
    def __init__(self, slots: int, reader_delay: Optional[int] = None):
        self.list = list(itertools.repeat(None, slots))
        self.write_ptr = 0

        if reader_delay is not None and reader_delay > slots:
            raise ValueError("Delay too big - it should be smaller or equal to the amount of slots provided")

        self.read_ptr = reader_delay or 0

    def iter_reverse(self):
        # FIXME: this isn't working..?
        # TODO: full failproof against data races (except for the actual data inside)

        safe_rptr_copy = self.read_ptr
        rptr = self.read_ptr

        if self.list[rptr] is None:
            return
        yield self.list[rptr]

        rptr -= 1
        if rptr < 0:
            rptr = len(self.list) - 1

        while rptr != safe_rptr_copy:
            yield self.list[rptr]
            rptr -= 1
            if rptr < 0:
                rptr = len(self.list) - 1

    def store(self, provided):
        if len(self.list) == 0:
            raise ValueError("Queue has no slots.")

        self.list[self.write_ptr] = provided
        self.write_ptr = (self.write_ptr + 1) % len(self.list)

    def exchange(self, provided):
        if len(self.list) == 0:
            raise ValueError("Queue has no slots.")

        read_item = self.list[self.read_ptr]
        self.read_ptr = (self.read_ptr + 1) % len(self.list)

        self.store(provided)

        return read_item

    def get(self, idx):
        return self.list[idx]

    def set(self, idx, val):
        self.list[idx] = val

    def len(self):
        return len(self.list)

if __name__ == "__main__":
    main()
