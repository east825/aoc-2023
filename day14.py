from aoc_toolkit import open_puzzle_input

NUM_CYCLES = 1_000_000_000


def transpose(block: list[str]) -> list[str]:
    return ["".join(row[col_idx] for row in block) for col_idx in range(len(block[0]))]


def flip_vertical(block: list[str]) -> list[str]:
    return block[::-1]


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


def slides_stones_east(platform: list[str]) -> list[str]:
    return transpose(
        flip_vertical(slide_stones_north(flip_vertical(transpose(platform))))
    )


def slides_stones_south(platform: list[str]) -> list[str]:
    return flip_vertical(slide_stones_north(flip_vertical(platform)))


def slides_stones_west(platform: list[str]) -> list[str]:
    return transpose(slide_stones_north(transpose(platform)))


def spin(platform: list[str]) -> list[str]:
    platform = slide_stones_north(platform)
    platform = slides_stones_west(platform)
    platform = slides_stones_south(platform)
    platform = slides_stones_east(platform)
    return platform


def calculate_load(platform: list[str]) -> int:
    return sum(
        len(platform) - row_idx
        for row_idx, row in enumerate(platform)
        for c in row
        if c == "O"
    )


def part1(puzzle_input: list[str]) -> int:
    return calculate_load(slide_stones_north(puzzle_input))


def part2(puzzle_input: list[str]) -> int:
    platform_state = tuple(puzzle_input)
    seen = {tuple(platform_state): 0}
    loop_size = 0
    for cycle in range(1, NUM_CYCLES + 1):
        platform_state = spin(platform_state)
        frozen_state = tuple(platform_state)
        if frozen_state in seen:
            loop_size = cycle - seen[frozen_state]
            break
        seen[frozen_state] = cycle
    remaining_cycles = (NUM_CYCLES - cycle) % loop_size
    for _ in range(remaining_cycles):
        platform_state = spin(platform_state)
    return calculate_load(platform_state)


if __name__ == "__main__":
    with open_puzzle_input("day14") as f:
        puzzle = f.read().splitlines()
        print(part1(puzzle))  # 108840
        print(part2(puzzle))  # 103445
