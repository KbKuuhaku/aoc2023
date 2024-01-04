import re

digit_pattern = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))")

str2val = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def solve(lines: list[str]) -> int:
    """
    On each row, Find the first digit and last digit and sum them
    Adding all sums will give you the answer
    """

    def get_digits(line: str) -> list[str]:
        digits = digit_pattern.findall(line)
        return digits

    str2val.update({s: index for index, s in enumerate("0123456789")})
    print(str2val)

    sum = 0
    for line in lines:
        digits = get_digits(line)

        if not digits:
            continue

        row_sum = 10 * str2val[digits[0]] + str2val[digits[-1]]
        sum += row_sum

    return sum


def process_input() -> list[str]:
    with open("inputs/day1.txt", "r") as f:
        lines = f.readlines()

    return lines


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
