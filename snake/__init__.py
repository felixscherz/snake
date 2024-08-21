from __future__ import annotations

import argparse
import curses
import random
from curses import wrapper
from enum import Enum
from enum import auto
from io import StringIO
from time import sleep
from typing import Optional
import logging 

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class GameLost(Exception): ...


class Cell: ...


class Segment(Cell):
    def __init__(self, age: int) -> None:
        """Creates a new snake segment."""
        super().__init__()
        self.age = age

    def tick(self, length: int) -> Cell:
        self.age += 1
        if self.age > length:
            return Empty()
        return self


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()

    def can_switch_to(self, other: Direction) -> bool:
        match self:
            case Direction.LEFT:
                match other:
                    case Direction.RIGHT:
                        return False
                    case _:
                        return True
            case Direction.RIGHT:
                match other:
                    case Direction.LEFT:
                        return False
                    case _:
                        return True
            case Direction.UP:
                match other:
                    case Direction.DOWN:
                        return False
                    case _:
                        return True
            case Direction.DOWN:
                match other:
                    case Direction.UP:
                        return False
                    case _:
                        return True


class Head(Cell):
    def __init__(self, direction: Direction):
        self.direction = direction

    def tick(self) -> Cell:
        return Segment(0)


class Empty(Cell):
    def tick(self) -> Cell:
        return self


class Food(Cell): ...


class Board:
    def __init__(self, width: int, height: int) -> None:
        assert width > 0
        assert height > 0
        self.width = width
        self.height = height
        self.board: list[list[Cell]] = [[Empty() for _ in range(width)] for _ in range(height)]
        self.head = Head(direction=Direction.RIGHT)
        self.head_pos = (0, 0)
        self[self.head_pos] = self.head
        self.length = 1
        self.food=False

    def __getitem__(self, slice: tuple[int, int]) -> Cell:
        return self.board[slice[0]][slice[1]]

    def __setitem__(self, slice: tuple[int, int], value: Cell):
        self.board[slice[0]][slice[1]] = value

    def tick(self, direction: Optional[Direction] = None):
        if direction:
            if not self.head.direction.can_switch_to(direction):
                direction = self.head.direction
        else:
            direction = self.head.direction

        match direction:
            case direction.UP:
                next_pos = ((self.head_pos[0] - 1) % self.height, self.head_pos[1])
            case direction.DOWN:
                next_pos = ((self.head_pos[0] + 1) % self.height, self.head_pos[1])
            case direction.LEFT:
                next_pos = (self.head_pos[0], (self.head_pos[1] - 1) % self.width)
            case direction.RIGHT:
                next_pos = (self.head_pos[0], (self.head_pos[1] + 1) % self.width)

        x = random.randint(0, self.height - 1)
        y = random.randint(0, self.width - 1)

        if isinstance(self[x, y], Empty) and not self.food:
            self.food = True
            self[x, y] = Food()

        self.head = Head(direction)
        if isinstance(self[next_pos], Segment):
            raise GameLost()

        if isinstance(self[next_pos], Food):
            self.food = False
            self.length += 1

        self[next_pos] = self.head
        self[self.head_pos] = Segment(-1)
        for i in range(self.height):
            for j in range(self.width):
                if isinstance(self[i, j], Segment):
                    self[i, j] = self[i, j].tick(self.length)
        self.head_pos = next_pos

    def next_pos(self, direction: Optional[Direction] = None) -> tuple[int, int]: ...

    def __str__(self) -> str:
        out = StringIO()
        for row in self.board:
            out.write("|")
            for col in row:
                match col:
                    case Empty():
                        out.write(" ")
                    case Food():
                        out.write("x")
                    case Segment():
                        out.write("o")
                    case Head():
                        match col.direction:
                            case Direction.UP:
                                out.write("^")
                            case Direction.DOWN:
                                out.write("v")
                            case Direction.RIGHT:
                                out.write(">")
                            case Direction.LEFT:
                                out.write("<")

            out.write("|")
            out.write("\n")
        return out.getvalue()


def play(stdscr: curses.window, width:int, height:int, tick_rate:float):
    # Clear screen
    stdscr.clear()

    board = Board(width, height)

    last_key = None

    while True:
        stdscr.nodelay(True)
        key = stdscr.getch()
        match key:
            case curses.KEY_DOWN | 106:
                board.tick(Direction.DOWN)
            case curses.KEY_UP | 107:
                board.tick(Direction.UP)
            case curses.KEY_LEFT | 104:
                board.tick(Direction.LEFT)
            case curses.KEY_RIGHT | 108:
                board.tick(Direction.RIGHT)
            case 32:
                board.length += 1
                board.tick()
            case _:
                board.tick()

        if key is not curses.ERR:
            last_key = key

        stdscr.erase()
        stdscr.addstr(str(board))
        stdscr.addstr(f"score: {board.length}\n")
        stdscr.addstr(f"button pressed: {chr(last_key or 1)}")
        stdscr.refresh()

        sleep(tick_rate)
