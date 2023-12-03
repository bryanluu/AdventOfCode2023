#!/bin/python3
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

from enum import Enum
from functools import reduce


class CubeColor(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"


INSIDE_BAG = {CubeColor.RED: 12, CubeColor.GREEN: 13, CubeColor.BLUE: 14}


def game_set_is_impossible(game_set):
    color_counts = game_set.split(", ")
    for color_count in color_counts:
        count, color = color_count.split(" ")
        if int(count) > INSIDE_BAG[CubeColor(color)]:
            return True
    return False



def game_is_valid(game):
    game_sets = game.split("; ")
    for game_set in game_sets:
        if game_set_is_impossible(game_set):
            return False
    return True

def game_id_number_if_game_is_valid(line):
    game_id, game = line.split(": ")
    game_id_number = int(game_id.split(" ")[1])
    return game_id_number if game_is_valid(game) else 0


def solve_part_1(lines):
    result = 0
    for line in lines:
        result += game_id_number_if_game_is_valid(line.strip())
    return result


def compute_minimum_cube_set(min_cube_set, bag):
    for color, count in bag.items():
        if count > min_cube_set.get(CubeColor(color), 0):
            min_cube_set[CubeColor(color)] = count
    return min_cube_set


def parse_bag(cube_set_str):
    bag = {}
    color_counts = cube_set_str.split(", ")
    for color_count in color_counts:
        count, color = color_count.split(" ")
        bag[CubeColor(color)] = int(count)
    return bag


def power_of_cube_set(line):
    _, cube_sets = line.split(": ")
    bags = map(parse_bag, cube_sets.split("; "))
    minimum_cube_set = reduce(compute_minimum_cube_set, bags)
    power = 1
    for color in CubeColor:
        power *= minimum_cube_set[color]
    return power


def solve_part_2(lines):
    result = 0
    for line in lines:
        result += power_of_cube_set(line.strip())
    return result


if __name__ == "__main__":
    print(f"Input file: {filename}")
    import time

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
