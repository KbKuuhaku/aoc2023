"""
--- Day 11: Cosmic Expansion Part2 ---

The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""


import itertools
from dataclasses import dataclass
from typing import Generator

from rich import print

# IO constants
INPUT_FILE = "inputs/day11.txt"
# INPUT_FILE = "inputs/day11_sample.txt"


# Constants
EMPTY = "."
GALAXY = "#"
EXPAND_RATE = 1000000


@dataclass
class Space:
    val: str
    x_offset: int = 1
    y_offset: int = 1

    def expand_x(self, expand_rate: int) -> None:
        self.x_offset = expand_rate

    def expand_y(self, expand_rate: int) -> None:
        self.y_offset = expand_rate

    @property
    def is_galaxy(self) -> bool:
        return self.val == GALAXY


class Solution:

    def __init__(self) -> None:
        ...

    def solve(self,
              image: list[list[Space]]) -> int:
        """
        1. Expand rows and columns where only empty space exists
        2. Record coordinates of each galaxy (by offset)
        3. Calculate manhattan distance between each pair of galaxies
        """

        def expand_cosmic(image: list[list[Space]],
                          expand_rate: int = EXPAND_RATE) -> None:
            m = len(image)
            n = len(image[0])

            # Rows
            for y in range(m):
                if any(space.is_galaxy for space in image[y]):
                    continue
                # Expand rows
                for space in image[y]:
                    space.expand_y(expand_rate)

            # Cols
            for x in range(n):
                if any(row[x].is_galaxy for row in image):
                    continue
                # Expand columns
                for row in image:
                    space = row[x]
                    space.expand_x(expand_rate)

        def galaxies(image: list[list[Space]]) -> Generator[tuple[int, int], list[list[Space]], None]:
            coor_y = 0
            for row in image:
                coor_x = 0
                for space in row:
                    if space.is_galaxy:
                        yield coor_y, coor_x
                    coor_x += space.x_offset

                coor_y += row[0].y_offset

        def manhattan_distance(p1: tuple[int, int],
                               p2: tuple[int, int]) -> int:
            y1, x1 = p1
            y2, x2 = p2

            return abs(y1 - y2) + abs(x1 - x2)

        # Expand the universe!
        expand_cosmic(image)

        # Calculate each pair of galaxies
        sum_of_dist = 0
        for g1, g2 in itertools.combinations(galaxies(image), r=2):
            sum_of_dist += manhattan_distance(g1, g2)

        return sum_of_dist


def process_input() -> list[list[Space]]:

    with open(INPUT_FILE, "r") as f:
        lines = [list(line.strip()) for line in f.readlines()]
        # print(lines)
        image = [[Space(val=char) for char in line]
                 for line in lines]

    return image


def main() -> None:
    print(Solution().solve(process_input()))


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(f"{(time.time() - start) * 1000} ms")
