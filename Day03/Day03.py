#!/bin/python3
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

import numpy as np
import re


class EngineSchematic:
    NUMBER_REGEX = r"(\d+)"
    SYMBOL_REGEX = r"([^0-9\.])"

    @property
    def part_numbers(self):
        """Returns all the numbers that are part numbers"""
        return [number for number in self.numbers if number["is_part"]]

    def is_near_pattern(self, number):
        """Returns whether a number is next to a pattern"""
        num_start = (number["row"], number["col"])
        num_end = (number["row"] + len(str(number["num"])), number["col"] + 1)
        p = re.compile(self.SYMBOL_REGEX)
        above_and_below = [
            (r, c)
            for r in [num_start[0] - 1, num_end[0]]
            for c in range(num_start[1] - 1, num_end[1])
            if r >= 0 and r < self.height and c >= 0 and c < self.width
        ]
        sides = [(r, c) for r in [num_start[0]] for c in [num_start[1] - 1, num_end[1]]]
        # Loop through all the neighbours and check if any are symbols
        for row, col in above_and_below + sides:
            if p.match(self.grid[row, col]):
                return False

        # If we get here, we didn't find any symbols
        return True

    def find_numbers(self):
        """Find all the numbers in the schematic, including whether they are part numbers or not"""
        p = re.compile(self.NUMBER_REGEX)
        self.numbers = []

        for row, line in enumerate(self.raw_schematic.splitlines()):
            for m in p.finditer(line):
                num_str = m.group(1)
                col = m.start(1)
                number = {"row": row, "col": col, "num": int(num_str)}
                number["is_part"] = self.is_near_pattern(number)
                self.numbers.append(number)

    def parse_schematic(self):
        """Parse the schematic into a grid of symbols and numbers"""
        self.grid = np.array(
            [list(line.strip()) for line in self.raw_schematic.split("\n")]
        )
        self.width, self.height = self.grid.shape

    def __init__(self, raw_schematic):
        self.raw_schematic = raw_schematic
        self.parse_schematic()
        self.find_numbers()


def solve_part_1(lines):
    pass  # DO STUFF


def solve_part_2(lines):
    pass  # DO STUFF


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
