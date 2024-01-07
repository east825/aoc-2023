import enum
import functools
import typing
from collections import defaultdict

from aoc_toolkit import open_puzzle_input, Pos


class Dir(enum.Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


class Beam(typing.NamedTuple):
    pos: Pos
    dir: Dir


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


def move_beam(beam: Beam, grid: list[str]) -> Beam | None:
    drow, dcol = beam.dir.value
    new_pos = Pos(beam.pos.row + drow, beam.pos.col + dcol)
    height, width = len(grid), len(grid[0])
    if 0 <= new_pos.row < height and 0 <= new_pos.col < width:
        return Beam(new_pos, beam.dir)
    return None


def energized_tiles(start_beam: Beam, grid: list[str]) -> set[Pos]:
    @functools.cache
    def trace(beam: Beam) -> tuple[set[Beam], set[Beam]]:
        energized: set[Beam] = {beam}
        while True:
            tile = grid[beam.pos.row][beam.pos.col]
            new_beams = {
                b
                for d in TURNS[tile][beam.dir]
                if (b := move_beam(Beam(beam.pos, d), grid))
            }
            # A loop or a dead-end reached
            if energized > new_beams:
                return set(), energized
            energized |= new_beams
            match list(new_beams):
                case [b1, b2]:
                    return {b1, b2}, energized
                case [single]:
                    beam = single

    all_energized: set[Beam] = set()
    untraced_sources, traced_sources = {start_beam}, set()

    while untraced_sources:
        beam_src = untraced_sources.pop()
        new_sources, energized = trace(beam_src)
        traced_sources.add(beam_src)
        all_energized |= energized
        untraced_sources |= new_sources - traced_sources
    return {pos for pos, _ in all_energized}


def part1(grid: list[str]) -> int:
    return len(energized_tiles(Beam(Pos(0, 0), Dir.RIGHT), grid))


if __name__ == "__main__":
    with open_puzzle_input("day16") as f:
        puzzle = f.read().splitlines()
        print(part1(puzzle))  # 7067
        # print(part2(puzzle))  # ?
