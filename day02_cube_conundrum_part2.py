"""
--- Day 2: Cube Conundrum ---

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
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

    @property
    def power(self) -> int:
        return (self.ball_counter["red"]
                * self.ball_counter["green"]
                * self.ball_counter["blue"])

    def __repr__(self) -> str:
        return f"Game {self.game_no}, {self.ball_counter}"


def solve(lines: list[str]) -> int:

    sum = 0
    for line in lines:
        game = GameParser(line)
        # print(game)
        sum += game.power

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
