"""
--- Day 9: Mirage Maintenance ---

To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.

In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:

0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:

0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0
You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:

0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0
Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:

0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0
So, the next value of the first history is 18.

"""

from rich import print

INPUT_FILE = "inputs/day9.txt"
# INPUT_FILE = "inputs/day9_sample.txt"


def solve(hist_nums: list[list[int]]):

    def extrapolate(hist_row: list[int]) -> list[list[int]]:
        all_diffs = [hist_row]
        elements = set(hist_row)

        while elements != {0}:
            new_diffs = []
            diffs = all_diffs[-1]
            for index in range(len(diffs) - 1):
                new_diffs.append(diffs[index + 1] - diffs[index])

            elements = set(new_diffs)
            all_diffs.append(new_diffs)
            diffs = new_diffs

        return all_diffs

    total = 0
    for hist_row in hist_nums:
        all_diffs = extrapolate(hist_row)
        prediction = sum([all_diff[-1] for all_diff in all_diffs])
        total += prediction

    return total


def process_input() -> list[list[int]]:

    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    return [[int(num) for num in nums.strip().split()]
            for nums in lines]


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
