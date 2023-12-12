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

PIPE_ASCII = {
    "|": "│",
    "-": "─",
    "L": "└",
    "J": "┘",
    "7": "┐",
    "F": "┌",
    "S": "S",
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


def draw_contour(field: list[str], contour: list[Pos], inner_tiles: set[Pos]) -> None:
    contour_pipes = set(contour)
    new_field = []
    for row_idx, row in enumerate(field):
        for col_idx, col in enumerate(row):
            if Pos(row_idx, col_idx) in contour_pipes:
                new_field.append(PIPE_ASCII[field[row_idx][col_idx]])
            elif Pos(row_idx, col_idx) in inner_tiles:
                new_field.append("I")
            else:
                new_field.append(" ")
        new_field.append("\n")
    with open("input/day10_prettified.txt", "w") as f:
        f.write("".join(new_field))


def find_inner_tiles(field: list[str], contour: list[Pos]) -> set[Pos]:
    start_pos = contour[-1]
    start_connections = {
        Pos(contour[-2].col - start_pos.col, contour[-2].row - start_pos.row),
        Pos(contour[0].col - start_pos.col, contour[0].row - start_pos.row),
    }
    s_replacement = next(
        pipe
        for pipe, conn in PIPE_CONNECTIONS.items()
        if set(conn) == start_connections
    )

    inner_tiles = set()
    contour_set = set(contour)
    for row_idx, row in enumerate(field):
        inside = False
        prev_bend = None
        for col_idx, col in enumerate(row):
            pos = Pos(row_idx, col_idx)
            if pos in contour_set:
                pipe = field[row_idx][col_idx]
                if pipe == "S":
                    pipe = s_replacement
                if pipe in "FL":
                    prev_bend = pipe
                elif pipe in "7J":
                    assert prev_bend is not None
                    if prev_bend + pipe in ["FJ", "L7"]:
                        inside = not inside
                elif pipe in "|":
                    inside = not inside
            elif inside:
                inner_tiles.add(pos)
    return inner_tiles


def part1(puzzle_input: list[str]) -> int:
    contour = find_contour(puzzle_input)
    return len(contour) // 2


def part2(puzzle_input: list[str]) -> int:
    contour = find_contour(puzzle_input)
    inner_tiles = find_inner_tiles(puzzle_input, contour)
    # draw_contour(puzzle_input, contour, inner_tiles)
    return len(inner_tiles)


if __name__ == "__main__":
    with open_puzzle_input("day10") as f:
        puzzle_input = list(f.read().splitlines())
        print(part1(puzzle_input))  # 6697
        print(part2(puzzle_input))
