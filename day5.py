import functools
import itertools

from aoc_toolkit import open_puzzle_input, blank_separated_line_blocks

type RangeMap = list[tuple[range, range]]

UNREACHABLE = 10_000_000_000


def part1(puzzle_input: list[list[str]]):
    def parse_map(block: list[str]) -> RangeMap:
        range_pairs = []
        for line in block[1:]:
            dst_start, src_start, range_len = map(int, line.split())
            range_pairs.append((range(src_start, src_start + range_len), range(dst_start, dst_start + range_len)))
        range_pairs.sort(key=lambda x: x[0].start)
        return range_pairs

    seed_block, *map_blocks = puzzle_input
    seeds = [int(n) for n in seed_block[0].removeprefix("seeds: ").split()]
    maps = [parse_map(block) for block in map_blocks]

    def find_location(seed: int) -> int:
        def find_dst(start: int, map: RangeMap) -> int:
            # TODO Can use the binary sort here
            for start_range, end_range in map:
                if start in start_range:
                    return end_range.start + (start - start_range.start)
            return start

        return functools.reduce(find_dst, maps, seed)

    return min(find_location(seed) for seed in seeds)


def part2(puzzle_input: list[list[str]]):
    def parse_map(block: list[str]) -> RangeMap:
        range_pairs = []
        for line in block[1:]:
            dst_start, src_start, range_len = map(int, line.split())
            range_pairs.append((range(src_start, src_start + range_len), range(dst_start, dst_start + range_len)))
        range_pairs.sort(key=lambda x: x[0].start)
        padded_range_pairs = []
        prev_range_end = 0
        for src_range, dst_range in range_pairs:
            if src_range.start > prev_range_end:
                padded_range_pairs.append(
                    (range(prev_range_end, src_range.start), range(prev_range_end, src_range.start))
                )
            padded_range_pairs.append((src_range, dst_range))
            prev_range_end = src_range.stop
        padded_range_pairs.append((range(src_range.stop, UNREACHABLE), range(src_range.stop, UNREACHABLE)))
        return padded_range_pairs

    seed_block, *map_blocks = puzzle_input
    header_nums = [int(n) for n in seed_block[0].removeprefix("seeds: ").split()]
    seed_ranges = [range(s, s + size) for s, size in itertools.batched(header_nums, 2)]
    maps = [parse_map(block) for block in map_blocks]

    def find_locations(seed_ranges: list[range]) -> list[range]:
        def translate(range_: range, map: RangeMap) -> list[range]:
            result = []
            for src_range, dst_range in map:
                range_intersection = range(max(range_.start, src_range.start), min(range_.stop, src_range.stop))
                if not range_intersection:
                    if result:
                        break
                    continue
                new_start = dst_range.start + (range_intersection.start - src_range.start)
                result.append(range(new_start, new_start + len(range_intersection)))
            return result

        def batch_translate(ranges: list[range], map_: RangeMap) -> list[range]:
            return [tr for r in ranges for tr in translate(r, map_)]

        return functools.reduce(batch_translate, maps, seed_ranges)

    return min(r.start for r in find_locations(seed_ranges))


if __name__ == "__main__":
    with open_puzzle_input("day5") as f:
        puzzle_input = list(blank_separated_line_blocks(f))
        print(part2(puzzle_input))
