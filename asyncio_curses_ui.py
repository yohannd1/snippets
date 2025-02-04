# My second attempt at an async-friendly terminal interface.
#
# Uses curses instead of termios this time around, cuz I was testing this on
# Windows with a friend, I think

import curses
import asyncio
from dataclasses import dataclass
from typing import Any

@dataclass
class TextBuffer:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.pos = 0
        self.scroll = 0
        self.resize()

    def add_line(self, line: str):
        self.lines.append(line)
        if self.pos == len(self.lines) - 2:
            self.move_curs(self.pos + 1)

    def resize(self):
        self.height = curses.LINES - 1
        self.move_curs(self.pos) # force scroll update

    def move_curs(self, new_pos):
        self.pos = max(min(len(self.lines)-1, new_pos), 0)

        # adjust scroll based on the cursor pos
        if self.pos < self.scroll:
            self.scroll = self.pos
        if self.pos - self.scroll > self.height - 1:
            self.scroll = self.pos - self.height + 1

async def main():
    queue = asyncio.Queue()

    win = curses.initscr()
    win.nodelay(True)
    curses.cbreak()
    win.keypad(True)
    curses.noecho()

    global should_stop
    should_stop = False

    async def try_get_key() -> Any:
        """Returns none if failed."""
        try:
            return win.getkey()
        except:
            return None

    async def job_input() -> None:
        while not should_stop:
            key = await try_get_key()
            if key is None:
                await asyncio.sleep(0.001) # to keep this job from starving others
            else:
                await queue.put(("key", key))

    async def job_timed() -> None:
        i = 0
        while not should_stop:
            await queue.put(("message", f"Timed message #{i}"))
            await asyncio.sleep(0.5)
            i += 1

    async def job_receiver():
        """Receive messages from the queue and act accordingly"""

        # uhhhhhhhh
        global detail_buf
        global command

        loglist = []
        log_buf = TextBuffer(loglist)
        detail_buf = None
        command = None

        def process_item(item):
            global detail_buf
            global command
            global should_stop

            cbuf = detail_buf or log_buf
            match item:
                case ("message", msg):
                    log_buf.add_line(msg)
                case ("key", key):
                    if command is not None:
                        if key == "\n":
                            log_buf.add_line(f"Ran command {command}")
                            command = None
                            log_buf.move_curs(len(log_buf.lines) - 1)
                        elif key == "^[":
                            command = None
                        else:
                            command += key
                    else:
                        if key == "KEY_UP": cbuf.move_curs(cbuf.pos - 1)
                        if key == "KEY_DOWN": cbuf.move_curs(cbuf.pos + 1)
                        if key == "KEY_PPAGE": cbuf.move_curs(cbuf.pos - curses.LINES//2)
                        if key == "KEY_NPAGE": cbuf.move_curs(cbuf.pos + curses.LINES//2)
                        if key == "KEY_HOME": cbuf.move_curs(0)
                        if key == "KEY_END": cbuf.move_curs(len(cbuf.lines) - 1)
                        if key == "\n":
                            detail_buf = TextBuffer(list(cbuf.lines[cbuf.pos].split("\n")))
                        if key == "/":
                            command = ""
                        if key == "q":
                            if detail_buf:
                                detail_buf = None
                            else:
                                should_stop = True
                    if key == "KEY_RESIZE":
                        log_buf.resize()
                        if detail_buf: detail_buf.resize()
                case _: raise Exception("unreachable")
            queue.task_done()

        while True:
            global should_stop
            win.clear()

            cbuf = detail_buf or log_buf

            win.addstr(0, 0, repr([cbuf.scroll - cbuf.height]))

            # draw current buffer to screen
            i = cbuf.scroll
            while i < min(len(cbuf.lines), cbuf.scroll + cbuf.height):
                win.addstr(i - cbuf.scroll, 0, cbuf.lines[i][:curses.COLS])
                i += 1

            # draw bottom bar
            if command is not None:
                win.addstr(curses.LINES-1, 0, f"/{command}")
            else:
                win.addstr(curses.LINES-1, 0, "(Q)quit ; (Enter)details ; (/)command")
                win.move(cbuf.pos - cbuf.scroll, 0)

            win.refresh()

            if should_stop:
                return

            # wait for item in queue and process it
            it = await queue.get()
            process_item(it)

            # process all elements currently on the queue, effectively emptying it
            while not queue.empty():
                it = queue.get_nowait()
                process_item(it)

    senders = [job_input(), job_timed()]
    recv = job_receiver()
    await asyncio.gather(*senders, recv)
    await queue.join() # what does this do again
    curses.endwin()

if __name__ == "__main__":
    asyncio.run(main())
