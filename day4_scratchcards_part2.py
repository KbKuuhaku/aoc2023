"""
--- Day 4: Scratchcards ---

There's no such thing as "points". Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. So, if you win a copy of card 10 and it has 5 matching numbers, it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. This process repeats until none of the copies cause you to win any more cards. (Cards will never make you copy a card past the end of the table.)

This time, the above example goes differently:

Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11

Card 1 has four matching numbers, so you win one copy each of the next four cards: cards 2, 3, 4, and 5.
Your original card 2 has two matching numbers, so you win one copy each of cards 3 and 4.
Your copy of card 2 also wins one copy each of cards 3 and 4.
Your four instances of card 3 (one original and three copies) have two matching numbers, so you win four copies each of cards 4 and 5.
Your eight instances of card 4 (one original and seven copies) have one matching number, so you win eight copies of card 5.
Your fourteen instances of card 5 (one original and thirteen copies) have no matching numbers and win no more cards.
Your one instance of card 6 (one original) has no matching numbers and wins no more cards.
Once all of the originals and copies have been processed, you end up with 1 instance of card 1, 2 instances of card 2, 4 instances of card 3, 8 instances of card 4, 14 instances of card 5, and 1 instance of card 6. In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!

Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of scratchcards, how many total scratchcards do you end up with?
"""

from collections import defaultdict
from dataclasses import dataclass

from rich import print


@dataclass
class CardStat:
    matches: int = 0
    n_cards: int = 1


class CardSolver:

    def __init__(self, card: str) -> None:
        self._parse_card(card)

    def _parse_card(self, card) -> None:
        card_title, card_info = card.split(": ")

        self._parse_card_title(card_title)
        self._parse_card_info(card_info)

    def _parse_card_title(self, card_title: str) -> None:
        self.card_no = int(card_title.split()[1])

    def _parse_card_info(self, card_info: str) -> None:
        winner, scratch = card_info.split(" | ")
        self._parse_winner_card(winner)
        self._parse_scratch_card(scratch)

    def _parse_winner_card(self, winner: str) -> None:
        self.winner_numbers = set(winner.split())

    def _parse_scratch_card(self, scratch: str) -> None:
        self.scratch_numbers = scratch.split()

    @property
    def matches(self) -> int:
        _matches = 0
        for scratch_number in self.scratch_numbers:
            if scratch_number not in self.winner_numbers:
                continue
            _matches += 1

        return _matches

    def __repr__(self) -> str:
        return f"Card {self.card_no}; Winner: {self.winner_numbers}; Scratch: {self.scratch_numbers}"


def solve(cards: list[str]) -> int:

    card_no_to_stat = defaultdict(lambda: CardStat())
    total_cards = 0

    for card in cards:
        solver = CardSolver(card)

        # Current card status
        card_no = solver.card_no
        card_stat = card_no_to_stat[card_no]
        card_stat.matches = solver.matches

        print(f"Card {card_no}, {card_stat}")
        total_cards += card_stat.n_cards

        # Add copies to the following cards
        start = card_no + 1
        for following_card in range(start, start + card_stat.matches):
            # Each card will give a copy to the next card
            card_no_to_stat[following_card].n_cards += card_stat.n_cards

    return total_cards


def process_input() -> list[str]:
    with open("inputs/day4.txt", "r") as f:
        # with open("inputs/day4_sample.txt", "r") as f:
        cards = f.readlines()

    return cards


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
