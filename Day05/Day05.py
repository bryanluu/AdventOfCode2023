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


def apply_map_to_source_numbers(source_numbers: list, mappings_str: str) -> list:
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
    locations = reduce(apply_map_to_source_numbers, line_groups, seeds)

    return min(locations)


def parse_seed_ranges(line: str) -> list:
    """Parse a line of the form `seeds: start end start end` to a list of seed ranges"""
    header, ranges = line.split(":")
    seed_ranges = {}
    nums = list(map(int, ranges.split()))
    while nums:
        start, length = nums.pop(0), nums.pop(0)
        seed_ranges[start] = {"start": start, "length": length, "offset": 0}

    return seed_ranges


def map_source_range(source_ranges: dict, mapping: dict) -> dict:
    """Apply a mapping to the source_range"""
    start = mapping["lower"]
    end = mapping["upper"]
    mapped = source_ranges.copy()
    for src in source_ranges.values():
        # src starting point
        src_start = src["start"]
        # src ending point
        src_end = src_start + src["length"]
        # if fully outside of range, don't change range
        if src_end <= start or src_start >= end:
            continue

        # if fully inside of range
        if src_start >= start and src_end <= end:
            mapped[src_start]["offset"] += mapping["offset"]
        # elif src_start is inside but src_end is not
        elif src_start >= start and src_start <= end and src_end > end:
            mapped[src_start]["length"] = end - src_start
            mapped[src_start]["offset"] += mapping["offset"]
            # add the interval after range
            offset_outside = source_ranges.get(end, {"offset": 0})["offset"]
            mapped[end] = {
                "start": end,
                "offset": offset_outside,
                "length": src_end - end,
            }
        # elif src_end is inside but src_start is not
        elif src_start < start and src_end >= start and src_end <= end:
            # trim the interval before range
            mapped[src_start]["length"] = start - src_start
            # add the interval inside range
            mapped[start] = {
                "start": start,
                "offset": src["offset"] + mapping["offset"],
                "length": src_end - start,
            }
        # elif range is inside of src
        elif src_start < start and src_end > end:
            # trim the interval before range
            mapped[src_start]["length"] = start - src_start
            # add the interval inside range
            mapped[start] = {
                "start": start,
                "offset": src["offset"] + mapping["offset"],
                "length": end - start,
            }
            # add the interval after range
            offset_outside = source_ranges.get(end, {"offset": 0})["offset"]
            mapped[end] = {
                "start": end,
                "offset": offset_outside,
                "length": src_end - end,
            }
    return mapped


def apply_map_to_source_ranges(source_ranges: dict, mappings_str: str) -> list:
    """Apply a mapping given by the mappings_str to the source_ranges."""
    lines = mappings_str.split("\n")
    header = lines.pop(0)

    print("src:", source_ranges)
    for line in lines:
        mapping = parse_range_mapping(line)
        mapped = map_source_range(source_ranges, mapping)
        print(line, mapped)

    return mapped


def solve_part_2(lines):
    # get groups
    line_groups = "".join(lines).strip().split("\n\n")

    # initialize seeds
    seed_ranges = line_groups.pop(0)

    # apply maps to seeds to obtain locations
    locations = reduce(apply_map_to_source_ranges, line_groups, seed_ranges)

    return min(locations)


if __name__ == "__main__":
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
