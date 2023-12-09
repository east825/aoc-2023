import itertools

from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks


def _part_input(puzzle_input: list[list[str]]) -> tuple[str, dict[str, tuple[str, str]]]:
    instructions_block, net_block = puzzle_input
    instructions = instructions_block[0]
    net = {}
    for node_line in net_block:
        node, left_right_nodes = node_line.split(" = ")
        net[node] = tuple(left_right_nodes[1:-1].split(", "))
    return instructions, net  # type: ignore


def part1(puzzle_input: list[list[str]]) -> int:
    instructions, net = _part_input(puzzle_input)

    cur_node = "AAA"
    steps = 0
    for move in itertools.cycle(instructions):
        left, right = net[cur_node]
        cur_node = right if move == "R" else left
        steps += 1
        if cur_node == "ZZZ":
            break
    return steps


def part2(puzzle_input: list[list[str]]) -> int:
    instructions, net = _part_input(puzzle_input)

    cur_nodes = frozenset(node for node in net if node.endswith("A"))
    steps = 0
    # cache = set()
    for move in itertools.cycle(instructions):
        # state = frozenset(cur_nodes), move
        # assert state not in cache
        # cache.add(state)
        cur_nodes = frozenset(net[node][1] if move == "R" else net[node][0] for node in cur_nodes)
        steps += 1
        if all(node.endswith("Z") for node in cur_nodes):
            break
    return steps


if __name__ == "__main__":
    with open_puzzle_input("day8") as f:
        puzzle_input = list(blank_separated_line_blocks(f))
        # print(part1(puzzle_input))  # 13939
        print(part2(puzzle_input))
