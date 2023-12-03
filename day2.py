from collections import Counter
from typing import TextIO

from aoc_toolkit import open_puzzle_input


def part1(input_: TextIO) -> int:
    bag = Counter({'red': 12, 'green': 13, 'blue': 14})

    # E.g: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    possible_game_ids = []
    for line in input_:
        game_header, draw_sets_text = line.split(': ')
        game_id = int(game_header.removeprefix('Game '))
        draw_sets = []
        for draw_set_text in draw_sets_text.split('; '):
            color_draws = Counter()
            for color_draw_text in draw_set_text.split(', '):
                cube_num, cube_color = color_draw_text.split()
                color_draws[cube_color] = int(cube_num)
            draw_sets.append(color_draws)
        if all(draw_set <= bag for draw_set in draw_sets):
            possible_game_ids.append(game_id)
    return sum(possible_game_ids)


if __name__ == '__main__':
    with open_puzzle_input('day2') as f:
        print(part1(f))
