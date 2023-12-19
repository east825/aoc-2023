import bisect
import itertools

from aoc_toolkit import open_puzzle_input, Pos


def expand(galaxies: list[Pos], image: list[str], factor: int) -> list[Pos]:
    width = len(image[0])
    empty_columns = [
        col for col in range(width) if all(row[col] == "." for row in image)
    ]
    empty_rows = [i for i, row in enumerate(image) if all(c == "." for c in row)]

    def offset(pos: Pos) -> Pos:
        empty_rows_before = bisect.bisect_left(empty_rows, pos.row)
        empty_columns_before = bisect.bisect_left(empty_columns, pos.col)
        return Pos(
            pos.row + empty_rows_before * (factor - 1),
            pos.col + empty_columns_before * (factor - 1),
        )

    return [offset(p) for p in galaxies]


def dist(pos1: Pos, pos2: Pos) -> int:
    return abs(pos2.col - pos1.col) + abs(pos2.row - pos1.row)


def find_galaxies(image):
    galaxies = [
        Pos(row_idx, col_idx)
        for row_idx, row in enumerate(image)
        for col_idx, char in enumerate(image[row_idx])
        if char == "#"
    ]
    return galaxies


def part1(image: list[str]) -> int:
    galaxies = find_galaxies(image)
    return sum(
        dist(g1, g2) for g1, g2 in itertools.combinations(expand(galaxies, image, 2), 2)
    )


def part2(image: list[str]) -> int:
    galaxies = find_galaxies(image)
    return sum(
        dist(g1, g2)
        for g1, g2 in itertools.combinations(expand(galaxies, image, 1_000_000), 2)
    )


if __name__ == "__main__":
    with open_puzzle_input("day11") as f:
        puzzle_input = f.read().splitlines()
        print(part1(puzzle_input))  # 9522407
        print(part2(puzzle_input))  # # 544723432977
