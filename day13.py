from functools import partial
from typing import Callable

from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks


def find_reflections(
    block: list[str], is_reflection_above: Callable[[list[str], int], bool]
) -> tuple[int, int]:
    transposed = ["".join(row[col] for row in block) for col in range(len(block[0]))]

    def rows_above_reflection(block: list[str]) -> int:
        for row_under_refl in range(1, len(block)):
            if is_reflection_above(block, row_under_refl):
                return row_under_refl
        return 0

    return rows_above_reflection(block), rows_above_reflection(transposed)


def is_perfect_reflection(block: list[str], row_below: int) -> bool:
    return all(
        r1 == r2 for r1, r2 in zip(block[row_below - 1 :: -1], block[row_below:])
    )


def is_reflection_with_smudge(block: list[str], row_below: int) -> bool:
    diff_count = sum(
        c1 != c2
        for r1, r2 in zip(block[row_below - 1 :: -1], block[row_below:])
        for c1, c2 in zip(r1, r2)
    )
    return diff_count == 1


def part1(puzzle_input: list[list[str]]) -> int:
    find = partial(find_reflections, is_reflection_above=is_perfect_reflection)
    return sum(100 * rows + columns for rows, columns in map(find, puzzle_input))


def part2(puzzle_input: list[list[str]]) -> int:
    find = partial(find_reflections, is_reflection_above=is_reflection_with_smudge)
    return sum(100 * rows + columns for rows, columns in map(find, puzzle_input))


if __name__ == "__main__":
    with open_puzzle_input("day13") as f:
        puzzle = list(blank_separated_line_blocks(f))
        print(part1(puzzle))  # 27742
        print(part2(puzzle))  # 32728
