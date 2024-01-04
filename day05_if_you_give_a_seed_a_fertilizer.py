"""
--- Day 5: If You Give A Seed A Fertilizer ---

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from dataclasses import dataclass, field

from rich import print


@dataclass
class RangeMap:
    """
    Store mappings that:
    start <= src < end, dest = src + map_offset
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

    def __getitem__(self, seed: int) -> int:
        return self._get_location_by_seed(seed)

    def _get_location_by_seed(self, seed: int) -> int:
        soil = _get(self.seed_to_soil, seed)
        fertilizer = _get(self.soil_to_fertilizer, soil)
        water = _get(self.fertilizer_to_water, fertilizer)
        light = _get(self.water_to_light, water)
        temperature = _get(self.light_to_temperature, light)
        humidity = _get(self.temperature_to_humidity, temperature)
        location = _get(self.humidity_to_location, humidity)

        return int(location)


def _get(range_maps: list[RangeMap],
         src: int) -> int:
    for range_map in range_maps:
        if range_map.within_range(src):
            return range_map[src]

    return src


class AlmanacParser:

    def __init__(self, almanac_list: list[str]) -> None:
        self.almanac = Almanac()
        self.current_range_maps = []

        self.title_to_range_maps = {
            "seed-to-soil": self.almanac.seed_to_soil,
            "soil-to-fertilizer": self.almanac.soil_to_fertilizer,
            "fertilizer-to-water": self.almanac.fertilizer_to_water,
            "water-to-light": self.almanac.water_to_light,
            "light-to-temperature": self.almanac.light_to_temperature,
            "temperature-to-humidity": self.almanac.temperature_to_humidity,
            "humidity-to-location": self.almanac.humidity_to_location,
        }

        self._parse_list(almanac_list)

    def _parse_list(self, almanac_list: list[str]) -> None:
        self._parse_seed(almanac_list[0])
        self._parse_maps(almanac_list[1:])

    def _parse_seed(self, seed_info: str) -> None:
        seeds = seed_info.split(": ")[1].split()
        self.seeds = [int(seed) for seed in seeds]

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
        return f"Seeds = {self.seeds};\n{self.almanac}"


def solve(almanac_list: list[str]) -> int:
    parser = AlmanacParser(almanac_list)
    # print(parser)

    lowest_location = float("inf")
    for seed in parser.seeds:
        lowest_location = min(lowest_location,
                              parser.almanac[seed])

    return lowest_location  # type: ignore


def process_input() -> list[str]:
    with open("inputs/day5.txt", "r") as f:
        # with open("inputs/day5_sample.txt", "r") as f:
        almanac_list = f.read().split("\n\n")

    return almanac_list


def main() -> None:
    print(solve(process_input()))


if __name__ == "__main__":
    main()
