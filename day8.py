import itertools
import math

from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks

type Net = dict[str, tuple[str, str]]


def _parse_input(puzzle_input: list[list[str]]) -> tuple[str, Net]:
    instructions_block, net_block = puzzle_input
    instructions = instructions_block[0]
    net = {}
    for node_line in net_block:
        node, left_right_nodes = node_line.split(" = ")
        net[node] = tuple(left_right_nodes[1:-1].split(", "))
    return instructions, net  # type: ignore


def _walk(net: Net, instructions: str, start_node: str, until=lambda node: False):
    cur_node = start_node
    steps = 0
    for move in itertools.cycle(instructions):
        left, right = net[cur_node]
        cur_node = right if move == "R" else left
        steps += 1
        if until(cur_node):
            break
    return steps, cur_node


def part1(puzzle_input: list[list[str]]) -> int:
    instructions, net = _parse_input(puzzle_input)
    steps, _ = _walk(net, instructions, "AAA", lambda node: node == "ZZZ")
    return steps


def part2(puzzle_input: list[list[str]]) -> int:
    instructions, net = _parse_input(puzzle_input)
    start_nodes = [node for node in net if node.endswith("A")]
    cycle_lengths = [_walk(net, instructions, node, lambda node: node.endswith("Z"))[0] for node in start_nodes]
    return math.lcm(*cycle_lengths)


if __name__ == "__main__":
    with open_puzzle_input("day8") as f:
        puzzle_input = list(blank_separated_line_blocks(f))
        print(part1(puzzle_input))  # 13939
        print(part2(puzzle_input))  # 8906539031197
