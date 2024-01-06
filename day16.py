import enum
from collections import defaultdict

from aoc_toolkit import open_puzzle_input, Pos


class Dir(enum.Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


TURNS: dict[str, dict[Dir, list[Dir]]] = {
    "/": {
        Dir.UP: [Dir.RIGHT],
        Dir.RIGHT: [Dir.UP],
        Dir.DOWN: [Dir.LEFT],
        Dir.LEFT: [Dir.DOWN],
    },
    "\\": {
        Dir.UP: [Dir.LEFT],
        Dir.RIGHT: [Dir.DOWN],
        Dir.DOWN: [Dir.RIGHT],
        Dir.LEFT: [Dir.UP],
    },
    "-": {
        Dir.UP: [Dir.LEFT, Dir.RIGHT],
        Dir.RIGHT: [Dir.RIGHT],
        Dir.DOWN: [Dir.LEFT, Dir.RIGHT],
        Dir.LEFT: [Dir.LEFT],
    },
    "|": {
        Dir.UP: [Dir.UP],
        Dir.RIGHT: [Dir.UP, Dir.DOWN],
        Dir.DOWN: [Dir.DOWN],
        Dir.LEFT: [Dir.UP, Dir.DOWN],
    },
    ".": {
        Dir.UP: [Dir.UP],
        Dir.RIGHT: [Dir.RIGHT],
        Dir.DOWN: [Dir.DOWN],
        Dir.LEFT: [Dir.LEFT],
    },
}


def move_pos(pos: Pos, direction: Dir, grid: list[str]) -> Pos | None:
    drow, dcol = direction.value
    new_pos = Pos(pos.row + drow, pos.col + dcol)
    height, width = len(grid), len(grid[0])
    return new_pos if 0 <= new_pos.row < height and 0 <= new_pos.col < width else None


def part1(grid: list[str]) -> int:
    energized_tiles: dict[Pos, set[Dir]] = defaultdict(set)
    energized_tiles[Pos(0, 0)].add(Dir.RIGHT)
    while True:
        total_beams = sum(map(len, energized_tiles.values()))
        for pos, beams in list(energized_tiles.items()):
            for beam_dir in beams:
                for next_dir in TURNS[grid[pos.row][pos.col]][beam_dir]:
                    next_pos = move_pos(pos, next_dir, grid)
                    if next_pos:
                        energized_tiles[next_pos].add(next_dir)
        if total_beams == sum(map(len, energized_tiles.values())):
            break
    return len(energized_tiles)


if __name__ == "__main__":
    with open_puzzle_input("day16") as f:
        puzzle = f.read().splitlines()
        print(part1(puzzle))  # 7067
        # print(part2(puzzle))  # ?
