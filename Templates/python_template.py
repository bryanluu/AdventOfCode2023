#!/bin/python3
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

def solve_part_1(lines):
    pass # DO STUFF

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
