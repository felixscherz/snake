from __future__ import annotations

from io import StringIO
from curses import wrapper
from enum import Enum
from enum import auto
from typing import Any
from typing import Optional


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

    def __getitem__(self, slice: tuple[int, int]) -> Cell:
        return self.board[slice[0]][slice[1]]

    def __setitem__(self, slice: tuple[int, int], value: Cell):
        self.board[slice[0]][slice[1]] = value

    def tick(self, direction: Optional[Direction] = None):
        if direction:
            assert self.head.direction.can_switch_to(direction)
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

        self.head = Head(direction)
        self[next_pos] = self.head
        self[self.head_pos] = Segment(-1)
        for i in range(self.height):
            for j in range(self.width):
                if isinstance(self[i,j], Segment):
                    self[i,j] = self[i,j].tick(self.length)
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
                    case Segment():
                        out.write("o")
                    case Head():
                        out.write(">")
            out.write("|")
            out.write("\n")
        return out.getvalue()



def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 10):
        v = i - 10
        stdscr.addstr(i, 0, "10 divided by {} is {}".format(v, 10 / v))

    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    wrapper(main)
