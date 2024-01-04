"""
--- Day 8: Haunted Wasteland ---
It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

import re
from dataclasses import dataclass

from rich import print


@dataclass
class Neighbor:
    left: str
    right: str


INPUT_FILE = "inputs/day8.txt"
# INPUT_FILE = "inputs/day8_sample.txt"
SOURCE = "AAA"
TARGET = "ZZZ"


match_pattern = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")


def solve(instruction: str,
          node_to_neighbors: dict[str, Neighbor]):
    node = SOURCE
    steps = 0
    index = 0

    while node != TARGET:
        direction = instruction[index]
        neighbor = node_to_neighbors[node]

        if direction == "L":
            node = neighbor.left
        else:
            node = neighbor.right

        # print(direction, node)

        steps += 1
        index = (index + 1) % len(instruction)

    return steps


def process_input() -> tuple[str, dict[str, Neighbor]]:

    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    instruction = lines[0].strip()

    node_to_neighbor = create_node_to_neighbor(lines[2:])

    return instruction, node_to_neighbor


def create_node_to_neighbor(lines: list[str]) -> dict[str, Neighbor]:
    node_to_neighbor = {}
    for line in lines:
        search_result = match_pattern.match(line)
        if search_result is None:
            raise ValueError(f"Regex not working on {line}")

        current_val, left_val, right_val = search_result.groups()
        node_to_neighbor[current_val] = Neighbor(left_val, right_val)

    return node_to_neighbor


def main() -> None:
    print(solve(*process_input()))


if __name__ == "__main__":
    main()
