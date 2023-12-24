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
def allocate(springs: str, groups: tuple[int, ...]) -> list[str]:
    if not groups:
        if "#" in springs:
            return []
        return [springs.replace("?", ".")]
    first, *rest, = groups
    result = []
    for i in range(len(springs)):
        if "#" in springs[:i] or not re.match(rf'[#?]{{{first}}}([.?]|$)', springs[i:]):
            continue
        partial = (springs[:i].replace("?", ".") +
                   springs[i:i + first].replace("?", "#") +
                   springs[i + first: i + first + 1].replace("?", "."))
        result.extend([partial + suffix for suffix in allocate(springs[i + first + 1:], tuple(rest))])
    return result


def part1(puzzle_input: list[str]):
    records = parse_input(puzzle_input)
    return sum(len(list(allocate(*record))) for record in records)


if __name__ == '__main__':
    with open_puzzle_input("day12") as f:
        print(part1(f.read().splitlines()))
