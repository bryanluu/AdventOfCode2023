#!/bin/python3
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

from functools import reduce

def parse_range_mapping(line: str) -> dict:
    """Parse a line of the form `dest, src, len` to a range mapping"""
    dest, src, length = map(int, line.split())
    return {
        # inclusive lower bound
        "lower": src,
        # non-inclusive upper bound
        "upper": src + length,
        # offset
        "offset": dest - src,
    }

def apply_map(source_numbers: list, mappings_str: str) -> list:
    """Apply a mapping given by the mappings_str to the source_numbers."""
    lines = mappings_str.split("\n")
    header = lines.pop(0)

    # parse mapping line
    mapped = {i: i for i in source_numbers}
    for line in lines:
        mapping = parse_range_mapping(line)
        for src in source_numbers:
            if mapping["lower"] <= src < mapping["upper"]:
                mapped[src] = src + mapping["offset"]
    print(header, mapped)

    return [mapped[i] for i in source_numbers]


def solve_part_1(lines):
    # get groups
    line_groups = "".join(lines).strip().split("\n\n")

    # initialize seeds
    seeds = list(map(int, line_groups.pop(0).split()[1:]))

    # apply maps to seeds to obtain locations
    locations = reduce(apply_map, line_groups, seeds)

    return min(locations)

def solve_part_2(lines):
    pass # DO STUFF

if __name__ == '__main__':
    print(f"Input file: {filename}")
    import time

    lines = []
    with open(filename, "r") as file:
        lines = file.readlines()

    start = time.time()
    print(f"Part 1: {solve_part_1(lines)}")
    end = time.time()
    print(f"Solve time: {end-start} seconds")
    start = time.time()
    print(f"Part 2: {solve_part_2(lines)}")
    end = time.time()
    print(f"Solve time: {end-start} seconds")
