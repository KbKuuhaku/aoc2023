
"""
--- Day 12: Hot Springs ---

In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.

However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).

So, condition records with no unknown spring conditions might look like this:

#.#.### 1,1,3
.#...#....###. 1,1,3
.#.###.#.###### 1,3,1,6
####.#...#... 4,1,1
#....######..#####. 1,6,5
.###.##....# 3,2,1
However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:

???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.
"""


import itertools
from dataclasses import dataclass
from typing import Generator

from rich import print

# IO constants
INPUT_FILE = "inputs/day12.txt"
# INPUT_FILE = "inputs/day12_sample.txt"


# Constants
OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"


class Solution:

    def __init__(self) -> None:
        ...

    def solve(self,
              spring_records: list[tuple[list[str], list[int]]]) -> int:

        def is_correct(guess_record: list[str]) -> bool:
            arrangement = [len(group) for group in "".join(guess_record).split(OPERATIONAL) if group]

            return arrangement == correct_arrangement

        def backtrack(guess_record: list[str]) -> None:
            if len(guess_record) == len(record):
                if is_correct(guess_record):
                    self.arrangement += 1
                return

            spring = record[len(guess_record)]
            if spring != UNKNOWN:
                backtrack(guess_record + [spring])
                return

            for guess in (OPERATIONAL, DAMAGED):
                backtrack(guess_record + [guess])

        self.arrangement = 0
        for record, correct_arrangement in spring_records:
            backtrack([])

        return self.arrangement


def process_input() -> list[tuple[list[str], list[int]]]:

    def proc_line(line: str) -> tuple[list[str], list[int]]:
        springs, correct_arrangement = line.strip().split()
        return list(springs), list(map(int, correct_arrangement.split(",")))

    with open(INPUT_FILE, "r") as f:
        lines = [proc_line(line) for line in f.readlines()]

    return lines


def main() -> None:
    print(Solution().solve(process_input()))


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(f"{(time.time() - start) * 1000} ms")
