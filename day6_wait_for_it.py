"""
--- Day 6: Wait For It ---

The organizer brings you over to the area where the boat races are held. The boats are much smaller than you expected - they're actually toy boats, each with a big button on top. Holding down the button charges the boat, and releasing the button allows the boat to move. Boats move faster if their button was held longer, but time spent holding the button counts against the total race time. You can only hold the button at the start of the race, and boats don't move until the button is released.

For example:

Time:      7  15   30
Distance:  9  40  200
This document describes three races:

The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.
Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.

So, because the first race lasts 7 milliseconds, you only have a few options:

Don't hold the button at all (that is, hold it for 0 milliseconds) at the start of the race. The boat won't move; it will have traveled 0 millimeters by the end of the race.
Hold the button for 1 millisecond at the start of the race. Then, the boat will travel at a speed of 1 millimeter per millisecond for 6 milliseconds, reaching a total distance traveled of 6 millimeters.
Hold the button for 2 milliseconds, giving the boat a speed of 2 millimeters per millisecond. It will then get 5 milliseconds to move, reaching a total distance of 10 millimeters.
Hold the button for 3 milliseconds. After its remaining 4 milliseconds of travel time, the boat will have gone 12 millimeters.
Hold the button for 4 milliseconds. After its remaining 3 milliseconds of travel time, the boat will have gone 12 millimeters.
Hold the button for 5 milliseconds, causing the boat to travel a total of 10 millimeters.
Hold the button for 6 milliseconds, causing the boat to travel a total of 6 millimeters.
Hold the button for 7 milliseconds. That's the entire duration of the race. You never let go of the button. The boat can't move until you let go of the button. Please make sure you let go of the button so the boat gets to move. 0 millimeters.

Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.

In the second race, you could hold the button for at least 4 milliseconds and at most 11 milliseconds and beat the record, a total of 8 different ways to win.

In the third race, you could hold the button for at least 11 milliseconds and no more than 19 milliseconds and still beat the record, a total of 9 ways you could win.

To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?
"""

from rich import print

INPUT_FILE = "inputs/day6.txt"
# INPUT_FILE = "inputs/day6_sample.txt"


def solve(times: list[int],
          distances: list[int]) -> int:

    def compute_ways_to_beat_record(time_limit: int,
                                    current_record: int) -> int:
        """
        Number of ways to beat the current record
        The race is split into two parts:
        1. hold the button
        2. let the boat go

        """
        ways_to_beat = 0
        for button_hold in range(1, time_limit):
            remained = time_limit - button_hold
            traveled_distance = button_hold * remained

            if traveled_distance > current_record:  # go farther than the current record
                ways_to_beat += 1

        return ways_to_beat

    ways = 1
    for _time, dist in zip(times, distances):
        ways *= compute_ways_to_beat_record(_time, dist)

    return ways


def process_input() -> tuple[list[int], list[int]]:

    def get_nums(info: str) -> list[int]:
        return [int(item) for item in info.split()[1:]]

    with open(INPUT_FILE, "r") as f:
        time_info = f.readline()
        distance_info = f.readline()

    return get_nums(time_info), get_nums(distance_info)


def main() -> None:
    print(solve(*process_input()))


if __name__ == "__main__":
    main()
