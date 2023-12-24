from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks


def reflections2(block: list[str]) -> tuple[int, int]:
    transposed = ["".join(row[col] for row in block) for col in range(len(block[0]))]

    def is_reflection_below(row: int, block: list[str]) -> bool:
        return all(r1 == r2 for r1, r2 in zip(block[row::-1], block[row + 1:]))

    def rows_above_reflection(b: list[str]) -> list[int]:
        result = []
        for row_above in range(len(b) - 1):
            # Puzzle input guarantees there is only one reflection of each type per map
            if is_reflection_below(row_above, b):
                result.append(row_above + 1)
        return result or [0]

    rows_above = rows_above_reflection(block)
    cols_to_left = rows_above_reflection(transposed)
    assert len(rows_above) == 1 and len(cols_to_left) == 1
    return rows_above[0], cols_to_left[0]


def part1(puzzle_input: list[list[str]]) -> int:
    return sum(100 * rows + columns for rows, columns in map(reflections2, puzzle_input))


if __name__ == "__main__":
    with open_puzzle_input("day13") as f:
        print(part1(list(blank_separated_line_blocks(f))))
