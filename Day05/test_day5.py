import Day05 as sut

EXAMPLE_FILENAME = "example.txt"

def test_apply_map():
    seeds = [79, 14, 55, 13]
    seed_to_soil = ["seed-to-soil map:\n", "50 98 2\n", "52 50 48\n"]

    assert sut.apply_map(seeds, seed_to_soil) == [81, 14, 57, 13]

def test_part_1():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_1(lines) == 35

def test_part_2():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    # assert sut.solve_part_2(lines) == 467835
