from aoc_toolkit import open_puzzle_input, Pos

PIPE_CONNECTIONS = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(0, 1), (1, 0)],
    "S": [(-1, 0), (0, 1), (1, 0), (0, -1)],
    ".": [],
}


def find_contour(field: list[str]) -> list[Pos]:
    start_pos = next(
        Pos(row_idx, col_idx)
        for row_idx, row in enumerate(field)
        for col_idx, char in enumerate(row)
        if char == "S"
    )
    height, width = len(field), len(field[0])

    def next_pos(pos: Pos, prev_pos: Pos = None) -> list[Pos]:
        result = []
        for row_delta, col_delta in PIPE_CONNECTIONS[field[pos.row][pos.col]]:
            p = Pos(pos.row + row_delta, pos.col + col_delta)
            if not (0 <= p.row < height) or not (0 <= p.col <= width):
                continue
            # Adjacent cell pipe cannot be connected back, relevant for S
            if (-row_delta, -col_delta) not in PIPE_CONNECTIONS[field[p.row][p.col]]:
                continue
            if p != prev_pos:
                result.append(p)
        return result

    cur_pos, prev_pos = start_pos, None
    contour = []
    while True:
        cur_pos, prev_pos = next_pos(cur_pos, prev_pos=prev_pos)[0], cur_pos
        contour.append(cur_pos)
        if field[cur_pos.row][cur_pos.col] == "S":
            break
    return contour


def part1(puzzle_input: list[str]) -> int:
    contour = find_contour(puzzle_input)
    return len(contour) // 2


if __name__ == "__main__":
    with open_puzzle_input("day10") as f:
        puzzle_input = list(f.read().splitlines())
        print(part1(puzzle_input))  # 6697
        # print(part2(puzzle_input))
