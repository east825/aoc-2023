import functools
import math
import operator

from aoc_toolkit import open_puzzle_input


def number_of_ways_to_beat(time: int, distance: int) -> int:
    return len(range(math.floor((time - math.sqrt(time * time - 4 * distance)) / 2 + 1),
                     math.ceil((time + math.sqrt(time * time - 4 * distance)) / 2)))


def part1(puzzle_input: list[str]):
    times = [int(n) for n in puzzle_input[0].removeprefix("Time: ").split()]
    distances = [int(n) for n in puzzle_input[1].removeprefix("Distance: ").split()]
    n_ways = [number_of_ways_to_beat(t, d) for t, d in zip(times, distances)]
    return functools.reduce(operator.mul, n_ways)


def part2(puzzle_input: list[str]):
    time = int(''.join(puzzle_input[0].removeprefix("Time: ").split()))
    distance = int(''.join(puzzle_input[1].removeprefix("Distance: ").split()))
    return number_of_ways_to_beat(time, distance)


if __name__ == '__main__':
    with open_puzzle_input('day6') as f:
        puzzle_input = f.read().splitlines()
        print(part1(puzzle_input))
        print(part2(puzzle_input))
