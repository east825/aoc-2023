import re
import string
from typing import TextIO

from aoc_toolkit import open_puzzle_input

DIGITS = {c: c for c in string.digits} | {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

_digit_re = re.compile(r'|'.join(DIGITS) + r'|[0-9]')


def part1(input_: TextIO) -> int:
    def calibration_value(line: str) -> int:
        digits = [c for c in line if c.isdigit()]
        return int(digits[0] + digits[-1])

    return sum(calibration_value(line) for line in input_)


def part2(input_: TextIO) -> int:
    def calibration_value(line: str) -> int:
        # _digit_re.findall(line) doesn't handle overlaps such as "oneight" or "nineight"
        digits = [DIGITS[m.group(0)] for i in range(len(line)) if (m := _digit_re.match(line, pos=i))]
        return int(digits[0] + digits[-1])

    return sum(calibration_value(line) for line in input_)


if __name__ == '__main__':
    with open_puzzle_input('day1') as f:
        print(part2(f))
