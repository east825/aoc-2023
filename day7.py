import enum
from collections import Counter

from aoc_toolkit import open_puzzle_input


class HandType(enum.IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

    @staticmethod
    def of_hand(hand: str, with_jokers=False) -> "HandType":
        counts = Counter(hand)
        assert counts.total() == 5
        if with_jokers:
            jokers = counts["J"]
            if jokers:
                # A joker can be the most common card itself
                del counts["J"]
                top_card = counts.most_common(1)
                counts[top_card[0][0] if top_card else "A"] += jokers
        match sorted(counts.values()):
            case [5]:
                return HandType.FIVE_OF_A_KIND
            case [1, 4]:
                return HandType.FOUR_OF_A_KIND
            case [2, 3]:
                return HandType.FULL_HOUSE
            case [1, 1, 3]:
                return HandType.THREE_OF_A_KIND
            case [1, 2, 2]:
                return HandType.TWO_PAIR
            case [1, 1, 1, 2]:
                return HandType.ONE_PAIR
            case [1, 1, 1, 1, 1]:
                return HandType.HIGH_CARD
        raise ValueError


def hand_strength(
    hand: str, with_jokers=False
) -> tuple[HandType, int, int, int, int, int]:
    cards_by_strength = "J23456789TJQKA" if with_jokers else "23456789TJQKA"
    return HandType.of_hand(hand, with_jokers), *(cards_by_strength.index(c) for c in hand)  # type: ignore


def _parse_input(puzzle_input: list[str]) -> list[tuple[int, int]]:
    hand_to_bid = []
    for line in puzzle_input:
        hand, bid = line.split()
        hand_to_bid.append((hand, int(bid)))
    return hand_to_bid


def part1(puzzle_input: list[str]) -> int:
    hand_to_bid = _parse_input(puzzle_input)
    ranks = sorted(
        (hand for hand, _ in hand_to_bid),
        key=lambda h: hand_strength(h, with_jokers=False),
    )
    return sum((ranks.index(hand) + 1) * bid for hand, bid in hand_to_bid)


def part2(puzzle_input: list[str]) -> int:
    hand_to_bid = _parse_input(puzzle_input)
    ranks = sorted(
        (hand for hand, _ in hand_to_bid),
        key=lambda h: hand_strength(h, with_jokers=True),
    )
    return sum((ranks.index(hand) + 1) * bid for hand, bid in hand_to_bid)


if __name__ == "__main__":
    with open_puzzle_input("day7") as f:
        puzzle_input = f.read().splitlines()
        print(part1(puzzle_input))  # 249483956
        print(part2(puzzle_input))  # 252137472
