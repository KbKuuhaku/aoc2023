"""
--- Day 11: Cosmic Expansion ---
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
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
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

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


import numpy as np
from rich import print

# IO constants
INPUT_FILE = "inputs/day11.txt"
# INPUT_FILE = "inputs/day11_sample.txt"


EMPTY = 0
GALAXY = 1

_char_to_int = {
    ".": EMPTY,
    "#": GALAXY
}


class Solution:

    def __init__(self) -> None:
        ...

    def solve(self,
              image: list[list[int]]) -> int:
        """
        1. Expand rows and columns where only empty space exists
        2. Record coordinates of each galaxy
        3. Calculate manhattan distance between each pair of galaxies
        """

        def expand(image):
            """

            """
            expanded = []

            for row in image:
                expanded.append(row)

                if all(char == EMPTY for char in row):
                    expanded.append(row)

            return np.array(expanded)

        def get_galaxies(image) -> list[tuple[int, int]]:
            galaxies = []
            for y, row in enumerate(image):
                for x, char in enumerate(row):
                    if char == GALAXY:
                        galaxies.append((y, x))
            return galaxies

        def manhattan_distance(p1: tuple[int, int],
                               p2: tuple[int, int]) -> int:
            y1, x1 = p1
            y2, x2 = p2

            return abs(y1 - y2) + abs(x1 - x2)

        space_image = np.array(image)
        del image

        # Expand rows
        space_image = expand(space_image)
        # Expand columns
        space_image = expand(space_image.T).T

        # Record all galaxies
        galaxies = get_galaxies(space_image)

        # Calculate each pair of galaxies
        sum_of_dist = 0
        n = len(galaxies)
        for i in range(n):
            for j in range(i + 1, n):
                sum_of_dist += manhattan_distance(galaxies[i],
                                                  galaxies[j])

        return sum_of_dist


def process_input() -> list[list[int]]:

    with open(INPUT_FILE, "r") as f:
        lines = [[_char_to_int[char] for char in line.strip()]
                 for line in f.readlines()]

    return lines


def main() -> None:
    print(Solution().solve(process_input()))


if __name__ == "__main__":
    import time
    start = time.time()
    main()
    print(f"{(time.time() - start) * 1000} ms")
