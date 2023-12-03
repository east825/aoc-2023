import re
from typing import NamedTuple

from aoc_toolkit import open_puzzle_input

_number_re = re.compile(r'\d+')


class Pos(NamedTuple):
    row: int
    col: int


def part1(schematic: list[str]) -> int:
    part_numbers: dict[Pos, int] = {}
    for row_idx, row in enumerate(schematic):
        for col_idx, c in enumerate(row):
            if not c.isdigit() and c != '.':
                part_numbers.update(find_adjacent_numbers(schematic, Pos(row_idx, col_idx)))

    return sum(part_numbers.values())


def part2(schematic: list[str]) -> int:
    gears = []
    for row_idx, row in enumerate(schematic):
        for col_idx, c in enumerate(row):
            if c == '*':
                adjacent_numbers = list(find_adjacent_numbers(schematic, Pos(row_idx, col_idx)).values())
                if len(adjacent_numbers) == 2:
                    gears.append(adjacent_numbers[0] * adjacent_numbers[1])

    return sum(gears)


def find_adjacent_numbers(schematic: list[str], pos: Pos) -> dict[Pos, int]:
    height, width = len(schematic), len(schematic[0])
    result = {}
    for row_idx in range(max(0, pos.row - 1), min(pos.row + 2, height)):
        for col_idx in range(max(0, pos.col - 1), min(pos.col + 2, width)):
            row = schematic[row_idx]
            if row[col_idx].isdigit():
                while col_idx > 0 and row[col_idx - 1].isdigit():
                    col_idx -= 1
                num = int(_number_re.match(row, pos=col_idx).group())
                result[Pos(row_idx, col_idx)] = num
    return result


if __name__ == '__main__':
    with open_puzzle_input('day3') as f:
        schematic = f.read().splitlines()
        print(part1(schematic))
        print(part2(schematic))
