#!/bin/python3
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

import numpy as np
import re


class EngineSchematic:
    NUMBER_REGEX = r"(\d+)"
    SYMBOL_REGEX = r"([^0-9\.])"

    @property
    def gear_ratios(self):
        """Returns the gear ratios"""
        return {
            gear_pos: ratios[0] * ratios[1] for gear_pos, ratios in self.gears.items()
        }

    @property
    def gears(self):
        """Returns all the valid gears"""
        return {
            gear_pos: ratios
            for gear_pos, ratios in self.__gears.items()
            if len(self.__gears[gear_pos]) == 2
        }

    @property
    def part_numbers(self):
        """Returns all the numbers that are part numbers"""
        return [number for number in self.numbers if number["nearby_symbols"]]

    def get_neighbor_positions(self, number):
        """Returns the neighboring positions of the number"""
        start = number["start"]
        end = (number["start"][0] + 1, number["start"][1] + len(str(number["value"])))
        sides = [
            (r, c)
            for r in [start[0]]
            for c in [start[1] - 1, end[1]]
            if c >= 0 and c < self.width
        ]
        above_and_below = [
            (r, c)
            for r in [start[0] - 1, end[0]]
            for c in range(start[1] - 1, end[1] + 1)
            if r >= 0 and r < self.height and c >= 0 and c < self.width
        ]
        return sides + above_and_below

    def symbols_nearby(self, number):
        """Returns any symbols next to number"""
        p = re.compile(self.SYMBOL_REGEX)
        symbols = []
        for row, col in self.get_neighbor_positions(number):
            if p.match(self.grid[row, col]):
                symbol = {"pos": (row, col), "value": self.grid[row, col]}
                symbols.append(symbol)

        return symbols if len(symbols) > 0 else None

    def register_number_to_gear(self, number, gear):
        """Register the number to a gear"""
        self.__gears[gear["pos"]] = self.__gears.get(gear["pos"], [])
        self.__gears[gear["pos"]].append(number["value"])

    def register_nearby_gears(self, number):
        """Register the number to any gears nearby"""
        if number["nearby_symbols"]:
            for symbol in number["nearby_symbols"]:
                if symbol["value"] == "*":
                    self.register_number_to_gear(number, symbol)

    def find_numbers(self):
        """Find all the numbers in the schematic, extracting nearby symbols"""
        p = re.compile(self.NUMBER_REGEX)
        self.numbers = []
        self.__gears = {}

        for row, line in enumerate(self.raw_schematic.splitlines()):
            for m in p.finditer(line):
                num_str = m.group(1)
                col = m.start(1)
                number = {"start": (row, col), "value": int(num_str)}
                number["nearby_symbols"] = self.symbols_nearby(number)
                self.register_nearby_gears(number)
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
    raw_file_input = "\n".join(map(lambda line: line.strip(), lines))
    schematic = EngineSchematic(raw_file_input)
    return sum([number["value"] for number in schematic.part_numbers])


def solve_part_2(lines):
    raw_file_input = "\n".join(map(lambda line: line.strip(), lines))
    schematic = EngineSchematic(raw_file_input)
    return sum(schematic.gear_ratios.values())


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
