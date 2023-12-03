import functools
import operator
from collections import Counter
from dataclasses import dataclass
from typing import TextIO, Literal

from aoc_toolkit import open_puzzle_input

Color = Literal["red", "blue", "green"]
CubeSet = Counter[Color]


@dataclass
class Game:
    id: int
    draw_sets: list[CubeSet]


def parse_games(input_: TextIO) -> list[Game]:
    games = []
    for line in input_:
        # E.g: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        game_header, draw_sets_text = line.split(': ')
        game_id = int(game_header.removeprefix('Game '))
        draw_sets = []
        for draw_set_text in draw_sets_text.split('; '):
            num_color_pairs = [tuple(chunk.split()) for chunk in draw_set_text.split(', ')]
            draw_sets.append(Counter({color: int(num) for num, color in num_color_pairs}))
        games.append(Game(id=game_id, draw_sets=draw_sets))

    return games


def part1(input_: TextIO) -> int:
    bag = Counter({'red': 12, 'green': 13, 'blue': 14})

    def is_possible(game: Game):
        return all(draw_set <= bag for draw_set in game.draw_sets)

    games = parse_games(input_)
    return sum(game.id for game in games if is_possible(game))


def part2(input_: TextIO) -> int:
    games = parse_games(input_)

    def min_cube_set(game: Game) -> CubeSet:
        return functools.reduce(operator.or_, game.draw_sets)

    def set_power(set_: CubeSet) -> int:
        return set_['red'] * set_['green'] * set_['blue']

    return sum(set_power(min_cube_set(game)) for game in games)


if __name__ == '__main__':
    with open_puzzle_input('day2') as f:
        print(part2(f))
