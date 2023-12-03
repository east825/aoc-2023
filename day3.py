import re
from typing import TextIO, NamedTuple

from aoc_toolkit import open_puzzle_input

_number_re = re.compile(r'\d+')


class Pos(NamedTuple):
    row: int
    col: int


def part1(input_: TextIO) -> int:
    schematic = list(line.rstrip() for line in input_)

    def block(top_left: Pos, bottom_right: Pos) -> list[str]:
        first_row, first_col = max(0, top_left.row), max(0, top_left.col)
        return [row[first_col:bottom_right.col] for row in schematic[first_row:bottom_right.row]]

    def is_symbol(c: str) -> bool:
        return not c.isdigit() and c != '.'

    part_numbers = []
    for row_idx, row in enumerate(schematic):
        for match in _number_re.finditer(row):
            adjacent_block = block(top_left=Pos(row_idx - 1, match.start() - 1),
                                   bottom_right=Pos(row_idx + 2, match.end() + 1))
            if any(is_symbol(c) for c in ''.join(adjacent_block)):
                part_numbers.append(int(match.group()))

    return sum(part_numbers)


if __name__ == '__main__':
    with open_puzzle_input('day3') as f:
        print(part1(f))
