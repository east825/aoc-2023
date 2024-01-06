from aoc_toolkit import open_puzzle_input


def part1(puzzle_input: str) -> int:
    def hash_(s: str) -> int:
        result = 0
        for c in s:
            result = ((result + ord(c)) * 17) % 256
        return result

    return sum(hash_(step) for step in puzzle_input.split(","))


if __name__ == "__main__":
    with open_puzzle_input("day15") as f:
        puzzle = f.read().strip()
        print(part1(puzzle))  # 509167
