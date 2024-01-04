
"""
--- Day 10: Pipe Maze ---
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

"""


import math
from enum import Enum, auto

from rich import print

START = "S"
GROUND = "."

INPUT_FILE = "inputs/day10.txt"
# INPUT_FILE = "inputs/day10_sample.txt"


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


class Status(Enum):
    INIT = auto()
    VISITED = auto()


class Solution:

    def __init__(self) -> None:
        self.tile_to_directions = {
            "|": (Direction.NORTH, Direction.SOUTH),
            "-": (Direction.WEST, Direction.EAST),
            "L": (Direction.NORTH, Direction.EAST),
            "J": (Direction.NORTH, Direction.WEST),
            "7": (Direction.SOUTH, Direction.WEST),
            "F": (Direction.SOUTH, Direction.EAST),
        }

        self.directions_to_tile = {
            dirs: tile
            for tile, dirs in self.tile_to_directions.items()
        }

        self.should_include = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
            Direction.EAST: Direction.WEST,
        }

    def solve(self,
              source: tuple[int, int],
              tiles: list[list[str]]) -> int:
        """
        Detect the unique loop and return the half length of loop
        """

        def get_neighbor(y: int, x: int, direction: Direction) -> tuple[int, int]:
            dir_y, dir_x = direction.value
            neighbor = y + dir_y, x + dir_x

            return neighbor

        def oob(node: tuple[int, int]) -> bool:
            y, x = node
            y_oob = y < 0 or y >= len(tiles)
            x_oob = x < 0 or x >= len(tiles[0])

            return y_oob or x_oob

        def detect_cycle(node: tuple[int, int],
                         parent: tuple[int, int],
                         path_length: int = 0) -> bool:
            y, x = node
            tile = tiles[y][x]

            if tile == GROUND:
                return False

            if status[y][x] == Status.VISITED:
                self.farthest = math.ceil(path_length / 2)
                return True

            status[y][x] = Status.VISITED

            for direction in self.tile_to_directions[tile]:
                neighbor = get_neighbor(y, x, direction)

                if oob(neighbor):
                    continue
                if neighbor == parent:
                    continue

                if detect_cycle(neighbor, node, path_length + 1):
                    return True

            return False

        def guess_tile(y: int, x: int) -> str:
            directions = []
            for direction in Direction:
                neighbor = get_neighbor(y, x, direction)
                neighbor_y, neighbor_x = neighbor
                neighbor_tile = tiles[neighbor_y][neighbor_x]

                if neighbor_tile == GROUND:
                    continue

                if self.should_include[direction] in self.tile_to_directions[neighbor_tile]:
                    directions.append(direction)

            return self.directions_to_tile[tuple(directions)]

        self.farthest = 0
        m = len(tiles)
        n = len(tiles[0])

        # Guess the source tile
        y, x = source
        source_tile = guess_tile(y, x)
        # print(tiles)
        print(f"Guess the source tile: {source_tile}")
        tiles[y][x] = source_tile

        # DFS
        status = [[Status.INIT for _ in range(n)]
                  for _ in range(m)]
        detect_cycle(source, parent=source)

        return self.farthest


def process_input() -> tuple[tuple[int, int], list[list[str]]]:

    def get_source(lines: list[list[str]]) -> tuple[int, int]:
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == START:
                    return y, x
        return -1, -1

    with open(INPUT_FILE, "r") as f:
        lines = [list(line.strip()) for line in f.readlines()]

    source = get_source(lines)

    return source, lines


def main() -> None:
    print(Solution().solve(*process_input()))


if __name__ == "__main__":
    import sys
    import time
    start = time.time()
    sys.setrecursionlimit(200000)
    main()
    print(f"{(time.time() - start) * 1000} ms")
