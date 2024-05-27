## First attempt of an async terminal interface, using termios

import sys, termios, os
import asyncio
from select import select
from dataclasses import dataclass
from typing import Any, Callable
from enum import IntEnum

# TODO: check if stdin/stdout are terminals

class Message(IntEnum):
    CONTINUE = 0
    STOP = 1

@dataclass
class IOManager:
    input_stream: Any = sys.stdin
    output_stream: Any = sys.stderr

    async def start(
        input_handler: Callable[[str], Message],
        ctrlc_handler: Callable[[], Message],
    ):
        pass

def getpass(prompt: str = "Input: "):
    fd = sys.stdin.fileno()
    orig_termios = termios.tcgetattr(fd)
    new_termios = termios.tcgetattr(fd)
    new_termios[3] &= ~(termios.ICANON | termios.ECHO)
    new_termios[6][termios.VMIN] = 0
    new_termios[6][termios.VTIME] = 1

    # set to new termios
    termios.tcsetattr(fd, termios.TCSADRAIN, new_termios)

    async def terminput(queue: asyncio.Queue):
        while True:
            ch = sys.stdin.read(1)

            if ch == "\n":
                await queue.put(("finish", None))
                await asyncio.sleep(0)
                continue
            elif ch == "\x7f":
                await queue.put(("backspace", None))
                await asyncio.sleep(0)
            else:
                await queue.put(("input", ch))
                await asyncio.sleep(0)

    async def timedsender(queue: asyncio.Queue):
        while True:
            await queue.put(("message", "I'm a message!"))
            await asyncio.sleep(0.5)

    async def receiver(queue: asyncio.Queue):
        input_buffer = []

        sys.stdout.write(prompt)
        sys.stdout.flush()

        def clear_line():
            sys.stdout.write("\r")
            sys.stdout.write(" " * os.get_terminal_size().columns)
            sys.stdout.write("\r")
            sys.stdout.flush()

        def redraw_input_buffer():
            sys.stdout.write(prompt + "".join(input_buffer))
            sys.stdout.flush()

        while True:
            kind, content = await queue.get()

            if kind == "message":
                clear_line()
                sys.stdout.write(f"Message -- {content}\n")
                sys.stdout.flush()
                redraw_input_buffer()
            elif kind == "backspace":
                if len(input_buffer) > 0:
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                    input_buffer = input_buffer[:-1]
            elif kind == "input":
                sys.stdout.write(content)
                sys.stdout.flush()
                input_buffer += content
            elif kind == "finish":
                sys.stdout.write("\n")

                sys.stdout.write(f"INPUT FINISHED :: {repr(''.join(input_buffer))}\n")
                sys.stdout.flush()

                input_buffer.clear()
                redraw_input_buffer()
            else:
                raise ValueError(f"Unknown kind: {repr(kind)}")

            queue.task_done()

    async def main():
        queue = asyncio.Queue()

        senders = [terminput(queue), timedsender(queue)]
        recv = receiver(queue)
        await asyncio.gather(*senders, recv)

        await queue.join()
        recv.cancel()

    try:
        asyncio.run(main())
    finally:
        # reset to original termios
        termios.tcsetattr(fd, termios.TCSADRAIN, orig_termios)

getpass()
