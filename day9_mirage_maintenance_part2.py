"""
--- Day 9: Mirage Maintenance ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0
Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?

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

    def predict(all_diffs: list[list[int]]) -> int:
        prediction = 0
        for index, all_diff in enumerate(all_diffs):
            if index % 2 == 0:  # even
                num = all_diff[0]
            else:
                num = -all_diff[0]
            prediction += num

        return prediction

    total = 0
    for hist_row in hist_nums:
        all_diffs = extrapolate(hist_row)
        prediction = predict(all_diffs)
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
