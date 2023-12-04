from aoc_toolkit import open_puzzle_input


def matching_numbers(puzzle_input: list[str]):
    result = []
    for line in puzzle_input:
        _, scratch_card = line.split(":")
        winning_list_text, available_list_text = scratch_card.split(" | ")
        winning_nums = set(map(int, winning_list_text.split()))
        available_nums = set(map(int, available_list_text.split()))
        matching_nums = winning_nums & available_nums
        result.append(len(matching_nums))
    return result


def part1(puzzle_input: list[str]):
    return sum(2 ** (count - 1) for count in matching_numbers(puzzle_input) if count)


def part2(puzzle_input: list[str]):
    scratch_card_copies = [1] * len(puzzle_input)
    for card_num, count in enumerate(matching_numbers(puzzle_input)):
        if count:
            for i in range(card_num + 1, min(card_num + 1 + count, len(scratch_card_copies))):
                scratch_card_copies[i] += scratch_card_copies[card_num]

    return sum(scratch_card_copies)


if __name__ == '__main__':
    with open_puzzle_input('day4') as f:
        puzzle_input = f.read().splitlines()
        print(part1(puzzle_input))
        print(part2(puzzle_input))
