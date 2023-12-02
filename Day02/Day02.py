#!/bin/python3
import sys

filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

from enum import Enum
import re


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
    game_id, game = line.strip().split(": ")
    game_id_number = int(game_id.split(" ")[1])
    return game_id_number if game_is_valid(game) else 0


def solve(filename):
    with open(filename, "r") as file:
        result = 0
        for line in file:
            result += game_id_number_if_game_is_valid(line)
        print(f"Result: {result}")


if __name__ == "__main__":
    print(f"Input file: {filename}")
    import time

    start = time.time()
    solve(filename)
    end = time.time()
    print(f"Solve time: {end-start} seconds")
