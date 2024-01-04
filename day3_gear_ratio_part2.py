"""
--- Day 3: Gear Ratios ---
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

import string
from enum import Enum

from rich import print

REQUIRED_PART_NUMBERS = 2


class Direction(Enum):
    up = (-1, 0)
    down = (1, 0)
    left = (0, -1)
    right = (0, 1)
    up_left = (-1, -1)
    up_right = (-1, 1)
    down_left = (1, -1)
    down_right = (1, 1)


def solve(lines: list[str]) -> int:

    def collect_part_numbers(y: int, x: int) -> set[tuple[int, int, int]]:
        current_part_numbers = set()
        for dir in Direction:
            y_dir, x_dir = dir.value
            y_neighbor, x_neighbor = y + y_dir, x + x_dir

            if oob(y_neighbor, x_neighbor):
                continue

            if lines[y_neighbor][x_neighbor] not in string.digits:
                continue

            number = collect_part_number(y_neighbor, x_neighbor)

            current_part_numbers.add(number)

        return current_part_numbers if len(current_part_numbers) == REQUIRED_PART_NUMBERS else set()

    def oob(y: int, x: int) -> bool:
        y_oob = (y < 0 or y >= len(lines))
        x_oob = (x < 0 or x >= len(lines[0]))

        return y_oob or x_oob

    def collect_part_number(y: int, x: int) -> tuple[int, int, int]:
        # Left
        left = x - 1
        while left >= 0 and lines[y][left] in string.digits:
            left -= 1

        # Right
        right = x + 1
        while right < len(lines[y]) and lines[y][right] in string.digits:
            right += 1

        return (y, left + 1, right)

    def compute_gear_ratio(part_numbers: set[tuple[int, int, int]]) -> int:
        gear_ratio = 1
        for y, x_left, x_right in list(part_numbers):
            num = int(lines[y][x_left: x_right])
            gear_ratio *= num

        return gear_ratio

    symbols = set(r"""`~!@#$%^&*()_-+={[}}|\:;"'<,>?/""")
    part_numbers = set()

    # Collect part numbers on each row
    gear_ratio_sum = 0
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] not in symbols:
                continue
            part_numbers = collect_part_numbers(y, x)
            if not part_numbers:
                continue

            gear_ratio_sum += compute_gear_ratio(part_numbers)

    return gear_ratio_sum


def process_input() -> list[str]:
    with open("inputs/day3.txt", "r") as f:
        # with open("inputs/day3_sample.txt", "r") as f:
        lines = f.readlines()

    return lines


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
