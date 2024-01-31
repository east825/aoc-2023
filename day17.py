import heapq
import itertools
import math
from typing import Callable, Iterable

from aoc_toolkit import open_puzzle_input, Pos, Dir

type NeighbourFunc[Node] = Callable[[Node], Iterable[tuple[Node, int]]]
type CostMap[Node] = dict[Node, int]
type ParentMap[Node] = dict[Node, Node]


def dijkstra[Node](start: Node, adj: NeighbourFunc) -> tuple[CostMap, ParentMap]:
    distances = {start: 0}
    parents = {}
    tie_breaker = itertools.count()
    pqueue = [(0, next(tie_breaker), start)]
    seen = set()
    while pqueue:
        est, _, node = heapq.heappop(pqueue)
        if node in seen:
            continue
        seen.add(node)
        distances[node] = est
        for neighbor, weight in adj(node):
            new_est = distances[node] + weight
            if distances.get(neighbor, math.inf) > new_est:
                heapq.heappush(pqueue, (new_est, next(tie_breaker), neighbor))
                parents[neighbor] = node
    return distances, parents


type State = tuple[Pos, Dir]


def part1(grid: list[str]):
    height, width = len(grid), len(grid[0])

    def adj(node: State) -> list[tuple[State, int]]:
        result: list[tuple[State, int]] = []
        pos, prev_dir = node
        for dir_ in Dir:
            if prev_dir and dir_ in (prev_dir, prev_dir.opposite):
                continue
            heat_loss = 0
            for size in range(1, 4):
                drow, dcol = dir_.value
                new_pos = Pos(pos.row + drow * size, pos.col + dcol * size)
                if 0 <= new_pos.row < height and 0 <= new_pos.col < width:
                    heat_loss += int(grid[new_pos.row][new_pos.col])
                    result.append(((new_pos, dir_), heat_loss))
        return result

    start, finish = Pos(0, 0), Pos(height - 1, width - 1)
    distances, _ = dijkstra((start, Dir.RIGHT), adj)
    return min(dist for (pos, _), dist in distances.items() if pos == finish)


if __name__ == "__main__":
    with open_puzzle_input("day17") as f:
        puzzle = f.read().splitlines()
        print(part1(puzzle))  # ?
