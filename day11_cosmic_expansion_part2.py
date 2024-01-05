"""
--- Day 11: Cosmic Expansion ---
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 # .........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 # ...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
# ............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
# ....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
# at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""


import itertools
from dataclasses import dataclass
from typing import Generator

from rich import print

# IO constants
INPUT_FILE = "inputs/day11.txt"
# INPUT_FILE = "inputs/day11_sample.txt"


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

        def expand(image: list[list[Space]],
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
        expand(image)

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
