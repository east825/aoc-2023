from aoc_toolkit import open_puzzle_input


def part1(puzzle_input: list[str]) -> int:
    def slide_stones_north(platform: list[str]) -> list[str]:
        new_state = [list(row) for row in platform]
        for row_idx, row in enumerate(new_state):
            for col_idx, c in enumerate(row):
                if c == "O":
                    stone_row = row_idx
                    while stone_row > 0 and new_state[stone_row - 1][col_idx] == ".":
                        stone_row -= 1
                    new_state[row_idx][col_idx] = "."
                    new_state[stone_row][col_idx] = "O"
        return ["".join(row) for row in new_state]

    def calculate_load(platform: list[str]) -> int:
        load = 0
        for row_idx, row in enumerate(platform):
            for col_idx, c in enumerate(row):
                if c == "O":
                    load += len(platform) - row_idx
        return load

    return calculate_load(slide_stones_north(puzzle_input))


if __name__ == "__main__":
    with open_puzzle_input("day14") as f:
        puzzle = f.read().splitlines()
        print(part1(puzzle))
