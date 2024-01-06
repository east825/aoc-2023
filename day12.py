import functools
import re

from aoc_toolkit import open_puzzle_input


def parse_input(puzzle_input: list[str]) -> list[tuple[str, tuple[int, ...]]]:
    result = []
    for line in puzzle_input:
        springs, groups = line.split()
        result.append((springs, tuple(int(n) for n in groups.split(","))))
    return result


@functools.cache
def allocate(springs: str, groups: tuple[int, ...]) -> int:
    if not groups:
        return 0 if "#" in springs else 1
    first, *rest = groups
    result = 0
    for i in range(len(springs)):
        if "#" in springs[:i] or not re.match(rf"[#?]{{{first}}}([.?]|$)", springs[i:]):
            continue
        result += allocate(springs[i + first + 1 :], tuple(rest))
    return result


def part1(puzzle_input: list[str]):
    records = parse_input(puzzle_input)
    return sum(allocate(*record) for record in records)


def part2(puzzle_input: list[str]):
    records = parse_input(puzzle_input)
    return sum(
        allocate("?".join([springs] * 5), groups * 5) for springs, groups in records
    )


if __name__ == "__main__":
    with open_puzzle_input("day12") as f:
        puzzle = f.read().splitlines()
        print(part1(puzzle))  # 6981
        print(part2(puzzle))  # 4546215031609
