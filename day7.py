import enum
from collections import Counter

from aoc_toolkit import open_puzzle_input

CARDS = 'J23456789TJQKA'


class HandType(enum.IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

    @staticmethod
    def of_hand(hand: str) -> 'HandType':
        counts = Counter(hand)
        assert counts.total() == 5
        jokers = counts['J']
        if jokers:
            del counts['J']
            top_card = counts.most_common(1)
            counts[top_card[0][0] if top_card else 'A'] += jokers
        card_counts = sorted(counts.values())
        if card_counts == [5]:
            return HandType.FIVE_OF_A_KIND
        elif card_counts == [1, 4]:
            return HandType.FOUR_OF_A_KIND
        elif card_counts == [2, 3]:
            return HandType.FULL_HOUSE
        elif card_counts == [1, 1, 3]:
            return HandType.THREE_OF_A_KIND
        elif card_counts == [1, 2, 2]:
            return HandType.TWO_PAIR
        elif card_counts == [1, 1, 1, 2]:
            return HandType.ONE_PAIR
        elif card_counts == [1, 1, 1, 1, 1]:
            return HandType.HIGH_CARD
        raise ValueError


def hand_strength(hand: str) -> tuple[HandType, int, int, int, int, int]:
    return HandType.of_hand(hand), *(CARDS.index(c) for c in hand)  # type: ignore


def part1(puzzle_input: list[str]) -> int:
    hand_to_bid = []
    for line in puzzle_input:
        hand, bid = line.split()
        hand_to_bid.append((hand, int(bid)))

    ranks = sorted((hand for hand, _ in hand_to_bid), key=hand_strength)
    return sum((ranks.index(hand) + 1) * bid for hand, bid in hand_to_bid)


def part2(puzzle_input: list[str]) -> int:
    hand_to_bid = []
    for line in puzzle_input:
        hand, bid = line.split()
        hand_to_bid.append((hand, int(bid)))

    ranks = sorted((hand for hand, _ in hand_to_bid), key=hand_strength)
    return sum((ranks.index(hand) + 1) * bid for hand, bid in hand_to_bid)


if __name__ == '__main__':
    with open_puzzle_input('day7') as f:
        puzzle_input = f.read().splitlines()
        # print(part1(puzzle_input))
        print(part2(puzzle_input))
