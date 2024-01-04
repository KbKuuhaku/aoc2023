"""
--- Day 5: If You Give A Seed A Fertilizer ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from dataclasses import dataclass, field
from typing import Optional

from rich import print


@dataclass
class RangeMap:
    """
    Store mappings that:
    when `start <= src < end`, `dest = src + map_offset`
    """
    start: int
    end: int
    map_offset: int

    def within_range(self, num: int) -> bool:
        return self.start <= num < self.end

    def __getitem__(self, num: int) -> int:
        return num + self.map_offset


@dataclass
class Almanac:

    seed_to_soil: list[RangeMap] = field(default_factory=list)
    soil_to_fertilizer: list[RangeMap] = field(default_factory=list)
    fertilizer_to_water: list[RangeMap] = field(default_factory=list)
    water_to_light: list[RangeMap] = field(default_factory=list)
    light_to_temperature: list[RangeMap] = field(default_factory=list)
    temperature_to_humidity: list[RangeMap] = field(default_factory=list)
    humidity_to_location: list[RangeMap] = field(default_factory=list)

    def get_location_ranges_by_seed_ranges(self, seed_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        soil_ranges = _get(self.seed_to_soil, seed_ranges)
        fertilizer_ranges = _get(self.soil_to_fertilizer, soil_ranges)
        water_ranges = _get(self.fertilizer_to_water, fertilizer_ranges)
        light_ranges = _get(self.water_to_light, water_ranges)
        temperature_ranges = _get(self.light_to_temperature, light_ranges)
        humidity_ranges = _get(self.temperature_to_humidity, temperature_ranges)
        location_ranges = _get(self.humidity_to_location, humidity_ranges)

        return location_ranges


def _get(range_maps: list[RangeMap],
         src_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:

    def map_range(start: int, end: int) -> Optional[tuple[int, int]]:
        for range_map in range_maps:
            if range_map.within_range(start):
                dest_start = range_map[start]
                if range_map.within_range(end):
                    # Map the range
                    dest_end = range_map[end]
                    dest_ranges.append((dest_start, dest_end))
                    return

                dest_end = range_map[range_map.end - 1]
                dest_ranges.append((dest_start, dest_end))
                return range_map.end, end

            if range_map.within_range(end):
                dest_start = range_map[range_map.start]
                dest_end = range_map[end]
                dest_ranges.append((dest_start, dest_end))
                return start, range_map.start - 1

        dest_ranges.append((start, end))

    # print(f"Src: {src_ranges}")
    dest_ranges = []

    while src_ranges:
        src_start, src_end = src_ranges.pop()

        remained = map_range(src_start, src_end)
        if remained:
            src_ranges.append(remained)

    # print(f"Dest: {dest_ranges}")

    return dest_ranges


class AlmanacParser:

    def __init__(self, almanac_list: list[str]) -> None:
        self.almanac = Almanac()
        self.current_range_maps = []

        self.title_to_range_maps = {"seed-to-soil": self.almanac.seed_to_soil,
                                    "soil-to-fertilizer": self.almanac.soil_to_fertilizer,
                                    "fertilizer-to-water": self.almanac.fertilizer_to_water,
                                    "water-to-light": self.almanac.water_to_light,
                                    "light-to-temperature": self.almanac.light_to_temperature,
                                    "temperature-to-humidity": self.almanac.temperature_to_humidity,
                                    "humidity-to-location": self.almanac.humidity_to_location, }

        self._parse_list(almanac_list)

    def _parse_list(self, almanac_list: list[str]) -> None:
        self._parse_seed(almanac_list[0])
        self._parse_maps(almanac_list[1:])

    def _parse_seed(self, seed_info: str) -> None:
        numbers = seed_info.split(": ")[1].split()
        self.seed_ranges = []
        for index in range(0, len(numbers), 2):
            seed_start = int(numbers[index])
            range_len = int(numbers[index + 1])
            seed_end = seed_start + range_len - 1

            self.seed_ranges.append((seed_start, seed_end))

    def _parse_maps(self, map_info: list[str]) -> None:
        for _map in map_info:
            title, detail = _map.split(maxsplit=1)
            self.current_range_maps = self.title_to_range_maps[title]

            map_details = detail.split(":")[1].strip().split("\n")
            self._parse_map_details(map_details)

    def _parse_map_details(self,
                           map_details: list[str]) -> None:
        for map_detail in map_details:
            self._parse_map_detail(map_detail)

    def _parse_map_detail(self,
                          map_detail: str) -> None:
        dest_category, src_category, range_len = list(map(int, map_detail.split()))
        self.current_range_maps.append(RangeMap(start=src_category,
                                                end=src_category + range_len,
                                                map_offset=dest_category - src_category))

    def __repr__(self) -> str:
        return f"Seeds = {self.seed_ranges};\n{self.almanac}"


def solve(almanac_list: list[str]) -> int:
    parser = AlmanacParser(almanac_list)
    almanac = parser.almanac
    seed_ranges = parser.seed_ranges
    # print(parser)

    location_ranges = almanac.get_location_ranges_by_seed_ranges(seed_ranges)

    location_ranges.sort(key=lambda x: x[0])
    # print(location_ranges)
    lowest_location = location_ranges[0][0]

    return lowest_location


def process_input() -> list[str]:
    with open("inputs/day5.txt", "r") as f:
        # with open("inputs/day5_sample.txt", "r") as f:
        almanac_list = f.read().split("\n\n")

    return almanac_list


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
