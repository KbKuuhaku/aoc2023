"""
--- Day 7: Camel Cards ---

To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""

from collections import Counter

from rich import print

JOKER = "J"

CARD_IN_ORDER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", JOKER]
_card_to_strength = {card: -index for index, card in enumerate(CARD_IN_ORDER)}


INPUT_FILE = "inputs/day7.txt"
# INPUT_FILE = "inputs/day7_sample.txt"


def solve(hands_and_bits: list[tuple[str, int]]) -> int:
    # print(rank(hands_and_bits[-1]))

    hands_and_bits.sort(key=rank)

    # Compute bits
    bits = 0
    for index, hand_and_bit in enumerate(hands_and_bits):
        hand, bit = hand_and_bit
        bits += (index + 1) * bit

    return bits


def rank(hand_and_bit: tuple[str, int]) -> tuple[list[int], list[int]]:
    def get_type(hand: str) -> list[int]:
        card_counter = Counter(hand)

        if ((JOKER not in card_counter)
                or (set(hand) == {JOKER})):
            return [card_count for card, card_count in card_counter.most_common()]

        # Move jokers' count onto the top
        card_counter = dict(card_counter)
        joker_count = card_counter[JOKER]
        del card_counter[JOKER]

        card_counter = dict(sorted(card_counter.items(), key=lambda x: -x[1]))
        top_card = list(card_counter.keys())[0]
        card_counter[top_card] += joker_count

        return list(card_counter.values())

    def get_strength(hand: str) -> list[int]:
        return [_card_to_strength[card] for card in hand]

    hand, bit = hand_and_bit
    _type = get_type(hand)
    strength = get_strength(hand)

    return _type, strength


def process_input() -> list[tuple[str, int]]:

    def get_hand_and_bit(line: str) -> tuple[str, int]:
        hand, bit = line.split()
        return hand, int(bit)

    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    return [get_hand_and_bit(line) for line in lines]


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
