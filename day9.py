import itertools

from aoc_toolkit import open_puzzle_input


def calc_next_val(history: list[int]) -> int:
    diffs = [next_val - prev_val for prev_val, next_val in itertools.pairwise(history)]
    if all(d == 0 for d in diffs):
        return history[-1]
    return history[-1] + calc_next_val(diffs)


def part1(puzzle_input: list[str]) -> int:
    val_histories = [[int(x) for x in line.split()] for line in puzzle_input]
    return sum(calc_next_val(hist) for hist in val_histories)


def part2(puzzle_input: list[str]) -> int:
    val_histories = [[int(x) for x in line.split()] for line in puzzle_input]
    return sum(calc_next_val(list(reversed(hist))) for hist in val_histories)


if __name__ == "__main__":
    with open_puzzle_input("day9") as f:
        puzzle_input = list(f.read().splitlines())
        print(part1(puzzle_input))  # 2105961943
        print(part2(puzzle_input))  # 1019
