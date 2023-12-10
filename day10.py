from aoc_toolkit import open_puzzle_input, Pos

PIPE_CONNECTIONS = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(0, 1), (1, 0)],
    "S": [(-1, 0), (0, 1), (1, 0), (0, -1)],
}


def part1(field: list[str]) -> int:
    start_pos = [
        Pos(row_idx, col_idx) for row_idx, row in enumerate(field) for col_idx, char in enumerate(row) if char == "S"
    ][0]
    height, width = len(field), len(field[0])

    path = [start_pos]
    seen = set(start_pos)

    def dfs(pos: Pos, from_delta: tuple[int, int]):
        symbol = field[pos.row][pos.col]
        for row_delta, col_delta in PIPE_CONNECTIONS[symbol]:
            if from_delta == (row_delta, col_delta):
                continue
            if 0 <= pos.row + row_delta < height and 0 <= pos.col + col_delta < width:
                adj_pos = Pos(pos.row + row_delta, pos.col + col_delta)
                adj_char = field[adj_pos.row][adj_pos.col]
                if adj_char == ".":
                    continue
                from_delta = (-row_delta, -col_delta)
                if from_delta not in PIPE_CONNECTIONS[adj_char]:
                    continue
                if adj_pos in seen:
                    if len(path) > 2:
                        yield adj_pos
                    continue
                yield adj_pos
                seen.add(adj_pos)
                path.append(adj_pos)
                yield from dfs(adj_pos, from_delta)
                path.pop()
                seen.remove(adj_pos)

    for pos in dfs(start_pos, (0, 0)):
        if field[pos.row][pos.col] == "S":
            return len(path)


if __name__ == "__main__":
    with open_puzzle_input("day10") as f:
        puzzle_input = list(f.read().splitlines())
        print(part1(puzzle_input))
        # print(part2(puzzle_input))
