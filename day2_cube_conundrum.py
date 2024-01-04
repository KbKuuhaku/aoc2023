"""
--- Day 2: Cube Conundrum ---

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
"""


class GameParser:

    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14

    def __init__(self, game_info: str) -> None:
        self.ball_counter = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        self.parse_game_info(game_info)

    def parse_game_info(self, game_info: str) -> None:
        self.game_title, self.game = game_info.split(":")
        self._parse_game_title()
        self._parse_game()

    def _parse_game_title(self) -> None:
        no = self.game_title.split()[1]
        self.game_no = int(no)

    def _parse_game(self) -> None:
        for round in self.game.split(";"):
            round = round.strip()
            self._parse_round(round)

    def _parse_round(self, round: str) -> None:
        for pick in round.split(","):
            num, ball = pick.strip().split()
            self.ball_counter[ball] = max(self.ball_counter[ball],
                                          int(num))

    def is_valid(self) -> bool:
        return (self.ball_counter["red"] <= self.MAX_RED
                and self.ball_counter["green"] <= self.MAX_GREEN
                and self.ball_counter["blue"] <= self.MAX_BLUE)

    def __repr__(self) -> str:
        return f"Game {self.game_no}, {self.ball_counter}"


def solve(lines: list[str]) -> int:

    sum = 0
    for line in lines:
        game = GameParser(line)
        # print(game)
        if game.is_valid():
            sum += game.game_no

    return sum


def process_input() -> list[str]:
    with open("inputs/day2.txt", "r") as f:
        # with open("inputs/day2_sample.txt", "r") as f:
        lines = f.readlines()

    return lines


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
