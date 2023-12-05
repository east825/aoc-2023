import functools

from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks

RangeMap = list[tuple[range, range]]


def part1(puzzle_input: list[list[str]]):
    def parse_map(block: list[str]) -> RangeMap:
        range_pairs = []
        for line in block[1:]:
            dst_start, src_start, range_len = map(int, line.split())
            range_pairs.append((range(src_start, src_start + range_len),
                                range(dst_start, dst_start + range_len)))
        range_pairs.sort(key=lambda x: x[0].start)
        return range_pairs

    seed_block, *map_blocks = puzzle_input
    seeds = [int(n) for n in seed_block[0].removeprefix('seeds: ').split()]
    maps = [parse_map(block) for block in map_blocks]

    def find_location(seed: int) -> int:
        def find_dst(start: int, map: RangeMap) -> int:
            for start_range, end_range in map:
                if start in start_range:
                    return end_range.start + (start - start_range.start)
            return start

        return functools.reduce(find_dst, maps, seed)

    return min(find_location(seed) for seed in seeds)


if __name__ == '__main__':
    with open_puzzle_input('day5') as f:
        puzzle_input = list(blank_separated_line_blocks(f))
        print(part1(puzzle_input))
