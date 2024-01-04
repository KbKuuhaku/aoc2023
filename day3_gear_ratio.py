"""
--- Day 3: Gear Ratios ---
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

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
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

import string
from enum import Enum

from rich import print


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

    def collect_part_numbers(y: int, x: int) -> None:
        for dir in Direction:
            y_dir, x_dir = dir.value
            y_neighbor, x_neighbor = y + y_dir, x + x_dir

            if oob(y_neighbor, x_neighbor):
                continue

            if lines[y_neighbor][x_neighbor] not in string.digits:
                continue

            number = collect_part_number(y_neighbor, x_neighbor)

            if number in part_numbers:
                continue

            part_numbers.add(number)

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

    symbols = set(r"""`~!@#$%^&*()_-+={[}}|\:;"'<,>?/""")
    part_numbers = set()

    # Collect part numbers on each row
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] not in symbols:
                continue
            collect_part_numbers(y, x)

    print(sorted(part_numbers))

    # Add them up
    sum = 0
    for y, x_left, x_right in part_numbers:
        sum += int(lines[y][x_left: x_right])

    return sum


def process_input() -> list[str]:
    with open("inputs/day3.txt", "r") as f:
        # with open("inputs/day3_sample.txt", "r") as f:
        lines = f.readlines()

    return lines


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
