"""
--- Day 8: Haunted Wasteland Part2 ---
What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

Step 0: You are at 11A and 22A.
Step 1: You choose all of the left paths, leading you to 11B and 22B.
Step 2: You choose all of the right paths, leading you to 11Z and 22C.
Step 3: You choose all of the left paths, leading you to 11B and 22Z.
Step 4: You choose all of the right paths, leading you to 11Z and 22B.
Step 5: You choose all of the left paths, leading you to 11B and 22C.
Step 6: You choose all of the right paths, leading you to 11Z and 22Z.
So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?
"""

import math
import re
from dataclasses import dataclass

from rich import print


@dataclass
class Neighbor:
    left: str
    right: str


INPUT_FILE = "inputs/day8.txt"
# INPUT_FILE = "inputs/day8_sample2.txt"
START = "A"
END = "Z"


match_pattern = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")


def solve(instruction: str,
          sources: list[str],
          node_to_neighbors: dict[str, Neighbor]):

    def navigate_node(node: str) -> int:
        index = 0
        steps = 0

        while not node.endswith(END):
            direction = instruction[index]
            neighbor = node_to_neighbors[node]

            if direction == "L":
                node = neighbor.left
            else:
                node = neighbor.right

            steps += 1
            index = (index + 1) % len(instruction)

        return steps

    nodes = sources
    node_steps = []
    for node in nodes:
        node_steps.append(navigate_node(node))

    # Lowest common multiple of steps of nodes
    return math.lcm(*node_steps)


def process_input() -> tuple[str, list[str], dict[str, Neighbor]]:

    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()

    instruction = lines[0].strip()

    sources, node_to_neighbor = preprocess(lines[2:])

    return instruction, sources, node_to_neighbor


def preprocess(lines: list[str]) -> tuple[list[str], dict[str, Neighbor]]:
    node_to_neighbor = {}
    sources = []
    for line in lines:
        search_result = match_pattern.match(line)
        if search_result is None:
            raise ValueError(f"Regex not working on {line}")

        current_val, left_val, right_val = search_result.groups()
        node_to_neighbor[current_val] = Neighbor(left_val, right_val)

        if current_val.endswith(START):
            sources.append(current_val)

    return sources, node_to_neighbor


def main() -> None:
    print(solve(*process_input()))


if __name__ == "__main__":
    main()
