
"""
--- Day 10: Pipe Maze ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?


"""


from enum import Enum, auto

from rich import print

START = "S"
GROUND = "."

INPUT_FILE = "inputs/day10.txt"
# INPUT_FILE = "inputs/day10_sample2.txt"


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
                         path: list[tuple[int, int]]) -> bool:
            y, x = node
            tile = tiles[y][x]

            if tile == GROUND:
                return False

            if status[y][x] == Status.VISITED:
                self.loop = path.copy()
                return True

            status[y][x] = Status.VISITED

            for direction in self.tile_to_directions[tile]:
                neighbor = get_neighbor(y, x, direction)

                if oob(neighbor):
                    continue
                if neighbor == parent:
                    continue

                if detect_cycle(neighbor, node, path + [neighbor]):
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

        self.loop = []
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
        detect_cycle(source, parent=source, path=[source])

        # self._print_loop(m, n)

        area_of_loop = shoelace_formula(self.loop)
        interior_points = picks_theorem(boundary_points=len(self.loop),
                                        area=area_of_loop)

        return interior_points

    def _print_loop(self, m: int, n: int) -> None:
        print(self.loop)
        loop_mat = [
            ["  " for _ in range(n)]
            for _ in range(m)
        ]
        for index, (y, x) in enumerate(self.loop):
            loop_mat[y][x] = str(index).rjust(2)

        print(loop_mat)


def picks_theorem(boundary_points: int,
                  area: int) -> int:
    return (area + 1) - int(boundary_points / 2)


def shoelace_formula(loop: list[tuple[int, int]]) -> int:
    """
    The area of the loop
    """
    area = 0
    for index in range(len(loop) - 1):
        y1, x1 = loop[index]
        y2, x2 = loop[index + 1]

        area += (x1 * y2 - x2 * y1)

    return int(abs(area / 2))


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
