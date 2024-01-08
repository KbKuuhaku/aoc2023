
"""
--- Day 12: Hot Springs ---
As you look out at the field of springs, you feel like there are way more springs than the condition records list. When you examine the records, you discover that they were actually folded up this whole time!

To unfold the records, on each row, replace the list of spring conditions with five copies of itself (separated by ?) and replace the list of contiguous groups of damaged springs with five copies of itself (separated by ,).

So, this row:

.# 1
Would become:

.#?.#?.#?.#?.# 1,1,1,1,1
The first line of the above example would become:

???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3
In the above example, after unfolding, the number of possible arrangements for some rows is now much larger:

???.### 1,1,3 - 1 arrangement
.??..??...?##. 1,1,3 - 16384 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 16 arrangements
????.######..#####. 1,6,5 - 2500 arrangements
?###???????? 3,2,1 - 506250 arrangements
After unfolding, adding all of the possible arrangement counts together produces 525152.

Unfold your condition records; what is the new sum of possible arrangement counts?
"""

# Reference: https://github.com/crunkyball/AdventOfCode2023/blob/main/Source/Days/Day12.cpp#L73

from collections import deque
from dataclasses import dataclass

from rich import print

# IO constants
INPUT_FILE = "inputs/day12.txt"
# INPUT_FILE = "inputs/day12_sample.txt"


# Constants
FOLD_RATE = 5


class SpringState:
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"


@dataclass
class Row:

    __slots__ = ["spring_states", "damaged_groups"]

    spring_states: deque[str]
    damaged_groups: deque[int]

    @property
    def empty_spring_state(self) -> bool:
        return not self.spring_states

    @property
    def empty_damage_group(self) -> bool:
        return not self.damaged_groups

    @property
    def top_spring_state(self) -> str:
        return self.spring_states[0]

    @property
    def top_damaged_group(self) -> int:
        return self.damaged_groups[0]

    def __str__(self) -> str:
        return f"{tuple(self.spring_states)}, {tuple(self.damaged_groups)}"


class Solution:

    def __init__(self) -> None:
        self.cache = {}
        self.cache_hits = 0

    def solve(self, rows: list[Row]) -> int:

        total_arrangement = 0
        for row in rows:
            row = self.unfold(row)
            arrangement = self.count_arrangement(row)
            # print(f"{row}, {arrangement}")
            total_arrangement += arrangement
        # print(self.cache_hits)
        return total_arrangement

    def count_arrangement(self,
                          row: Row,
                          n_damaged: int = 0) -> int:
        key = (str(row), n_damaged)
        if key in self.cache:
            self.cache_hits += 1
            return self.cache[key]

        if row.empty_spring_state and row.empty_damage_group:
            arrangement = 1
            self.cache[key] = arrangement
            return arrangement

        if row.empty_spring_state:
            if n_damaged == row.top_damaged_group:
                top_damage_group = row.damaged_groups.popleft()

                arrangement = self.count_arrangement(row, n_damaged=0)

                row.damaged_groups.appendleft(top_damage_group)
            else:
                arrangement = 0
            self.cache[key] = arrangement
            return arrangement

        if row.empty_damage_group:
            arrangement = 0 if SpringState.DAMAGED in row.spring_states else 1
            self.cache[key] = arrangement
            return arrangement

        # Prune
        if n_damaged > row.top_damaged_group:
            arrangement = 0
            self.cache[key] = arrangement
            return arrangement

        arrangement = 0
        match (row.top_spring_state):
            case SpringState.OPERATIONAL:
                if n_damaged == row.top_damaged_group:  # aligned
                    top_spring_state = row.spring_states.popleft()
                    top_damage_group = row.damaged_groups.popleft()

                    arrangement = self.count_arrangement(row, n_damaged=0)

                    row.spring_states.appendleft(top_spring_state)
                    row.damaged_groups.appendleft(top_damage_group)
                elif n_damaged == 0:  # no damage group
                    top_spring_state = row.spring_states.popleft()

                    arrangement = self.count_arrangement(row, n_damaged=0)

                    row.spring_states.appendleft(top_spring_state)
                else:  # not aligned
                    arrangement = 0
            case SpringState.DAMAGED:
                top_spring_state = row.spring_states.popleft()

                arrangement = self.count_arrangement(row, n_damaged=n_damaged + 1)

                row.spring_states.appendleft(top_spring_state)
            case SpringState.UNKNOWN:
                for replace in (SpringState.OPERATIONAL, SpringState.DAMAGED):
                    row.spring_states[0] = replace
                    arrangement += self.count_arrangement(row, n_damaged=n_damaged)
                row.spring_states[0] = SpringState.UNKNOWN
            case _:
                raise ValueError(f"State {row.top_spring_state} is invalid")

        self.cache[key] = arrangement
        return arrangement

    @staticmethod
    def unfold(row: Row, fold_rate=FOLD_RATE) -> Row:
        spring_states = deque(SpringState.UNKNOWN.join(["".join(row.spring_states)] * fold_rate))
        damaged_groups = deque(row.damaged_groups * fold_rate)

        return Row(spring_states, damaged_groups)


def process_input() -> list[Row]:

    def proc_line(line: str) -> Row:
        spring_states, damaged_groups = line.strip().split()
        return Row(deque(spring_states),
                   deque(map(int, damaged_groups.split(","))))

    with open(INPUT_FILE, "r") as f:
        rows = [proc_line(line) for line in f.readlines()]

    return rows


def main() -> None:
    print(Solution().solve(process_input()))


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(f"{(time.time() - start) * 1000} ms")
