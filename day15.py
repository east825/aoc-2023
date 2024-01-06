import functools
import typing

from aoc_toolkit import open_puzzle_input


class Step(typing.NamedTuple):
    label: str
    op: str
    focal_len: int

    @classmethod
    def parse(cls, step: str) -> "Step":
        if "=" in step:
            label, focal = step.split("=")
            return Step(label, "=", int(focal))
        else:
            return Step(step.rstrip("-"), "-", -1)


def hash_(s: str) -> int:
    return functools.reduce(lambda res, c: ((res + ord(c)) * 17) % 256, s, 0)


def part1(puzzle_input: str) -> int:
    return sum(hash_(step) for step in puzzle_input.split(","))


def part2(puzzle_input: str) -> int:
    # Python 3.7+ dicts preserve the insertion order
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    for step in list(map(Step.parse, puzzle_input.split(","))):
        match step.op:
            case "-":
                boxes[hash_(step.label)].pop(step.label, None)
            case "=":
                boxes[hash_(step.label)][step.label] = step.focal_len

    result = 0
    for box_num, box in enumerate(boxes):
        for slot, (_, focal_len) in enumerate(box.items(), start=1):
            result += (box_num + 1) * slot * focal_len
    return result


if __name__ == "__main__":
    with open_puzzle_input("day15") as f:
        puzzle = f.read().strip()
        print(part1(puzzle))  # 509167
        print(part2(puzzle))  # 259333
