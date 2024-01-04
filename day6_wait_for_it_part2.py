"""
--- Day 6: Wait For It ---

As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200
...now instead means this:

Time:      71530
Distance:  940200
Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?
"""

from rich import print

INPUT_FILE = "inputs/day6.txt"
# INPUT_FILE = "inputs/day6_sample.txt"


def solve(time_limit: int,
          current_record: int) -> int:
    """
    Number of ways to beat the current record
    The race is split into two parts:
    1. hold the button
    2. let the boat go

    ==> Solve x * (a - x) > b, where a and b are constants

    ways = (x0+ - x0- + 1)
    """
    import math

    def solve_quad_equation(a: int,
                            b: int,
                            c: int) -> tuple[float, float]:
        delta = math.sqrt(b * b - 4 * a * c)
        x1 = (-b - delta) / (2 * a)
        x2 = (-b + delta) / (2 * a)

        return (x1, x2) if x1 < x2 else (x2, x1)

    left_bound, right_bound = solve_quad_equation(a=-1,
                                                  b=time_limit,
                                                  c=-current_record)
    left_bound = math.ceil(left_bound)
    right_bound = math.floor(right_bound)

    return (right_bound - left_bound + 1)


def process_input() -> tuple[int, int]:

    def get_num(info: str) -> int:
        return int("".join(info.split()[1:]))

    with open(INPUT_FILE, "r") as f:
        time_info = f.readline()
        distance_info = f.readline()

    return get_num(time_info), get_num(distance_info)


def main() -> None:
    print(solve(*process_input()))


if __name__ == "__main__":
    main()
