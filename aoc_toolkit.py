import enum
from pathlib import Path
from typing import TextIO, Generator, Any, NamedTuple

_root = Path(__file__).parent


def open_puzzle_input(name: str) -> TextIO:
    return (_root / "input" / f"{name}.txt").open(encoding="utf-8")


def blank_separated_line_blocks(file: TextIO) -> Generator[list[str], Any, Any]:
    block = []
    for line in file:
        line = line.rstrip()
        if not line:
            if block:
                yield block
                block = []
        else:
            block.append(line)
    if block:
        yield block


class Pos(NamedTuple):
    row: int
    col: int


class Dir(enum.Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
