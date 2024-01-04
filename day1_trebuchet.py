import sys


def solve(lines: list[str]) -> int:
    """
    On each row, Find the first digit and last digit and sum them
    Adding all sums will give you the answer
    """

    def get_digits(line: str) -> str:
        digits = ""
        for char in line:
            if char in ALL_DIGITS:
                digits += char

        return digits

    sum = 0
    ALL_DIGITS = "0123456789"
    for line in lines:
        digits = get_digits(line)

        if not digits:
            continue

        row_sum = 10 * int(digits[0]) + int(digits[-1])
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
