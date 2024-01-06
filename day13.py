from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks


def reflections(block: list[str]) -> tuple[int, int]:
    transposed = ["".join(row[col] for row in block) for col in range(len(block[0]))]

    def is_reflection_above(refl_row: int, block: list[str]) -> bool:
        return all(
            r1 == r2 for r1, r2 in zip(block[refl_row - 1 :: -1], block[refl_row:])
        )

    def rows_above_reflection(block: list[str]) -> int:
        for refl_size in range(len(block) // 2, 0, -1):
            for row_under_refl in refl_size, len(block) - refl_size:
                if is_reflection_above(row_under_refl, block):
                    return row_under_refl
        return 0

    return rows_above_reflection(block), rows_above_reflection(transposed)


def part1(puzzle_input: list[list[str]]) -> int:
    return sum(100 * rows + columns for rows, columns in map(reflections, puzzle_input))


if __name__ == "__main__":
    with open_puzzle_input("day13") as f:
        print(part1(list(blank_separated_line_blocks(f))))  # 27742
