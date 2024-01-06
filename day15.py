import functools

from aoc_toolkit import open_puzzle_input


def part1(puzzle_input: str) -> int:
    def hash_(s: str) -> int:
        return functools.reduce(lambda res, c: ((res + ord(c)) * 17) % 256, s, 0)

    return sum(hash_(step) for step in puzzle_input.split(","))


if __name__ == "__main__":
    with open_puzzle_input("day15") as f:
        puzzle = f.read().strip()
        print(part1(puzzle))  # 509167
