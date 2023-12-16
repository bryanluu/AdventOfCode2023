import Day05 as sut

EXAMPLE_FILENAME = "example.txt"


def test_parse_range_mapping():
    assert sut.parse_range_mapping("50 98 2") == {
        "lower": 98,
        "upper": 100,
        "offset": -48,
    }
    assert sut.parse_range_mapping("52 50 48") == {
        "lower": 50,
        "upper": 98,
        "offset": 2,
    }


def test_apply_map_to_source_numbers():
    seeds = [79, 14, 55, 13]
    seed_to_soil = "seed-to-soil map:\n50 98 2\n52 50 48"

    assert sut.apply_map_to_source_numbers(seeds, seed_to_soil) == [81, 14, 57, 13]


def test_part_1():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_1(lines) == 35


def test_parse_seed_ranges():
    line = "seeds: 79 14 55 13"
    assert sut.parse_seed_ranges(line) == {
        55: {"start": 55, "length": 13, "offset": 0},
        79: {"start": 79, "length": 14, "offset": 0},
    }


def test_map_source_range():
    case_A = {
        4: {"start": 4, "length": 2, "offset": 0},
        7: {"start": 7, "length": 3, "offset": 0},
    }
    case_B = {
        1: {"start": 1, "length": 4, "offset": 3},
        5: {"start": 5, "length": 7, "offset": 0},
    }
    mapping = {"lower": 6, "upper": 8, "offset": -4}

    assert sut.map_source_range(case_A, mapping) == {
        4: {"start": 4, "length": 2, "offset": 0},
        7: {"start": 7, "length": 1, "offset": -4},
        8: {"start": 8, "length": 2, "offset": 0},
    }
    assert sut.map_source_range(case_B, mapping) == {
        1: {"start": 1, "length": 4, "offset": 3},
        5: {"start": 5, "length": 1, "offset": 0},
        6: {"start": 6, "length": 2, "offset": -4},
        8: {"start": 8, "length": 4, "offset": 0},
    }


def test_update_mapped_ranges():
    mapped = {
        1: {"start": 1, "length": 1, "offset": 8},
        2: {"start": 2, "length": 2, "offset": 4},
        4: {"start": 4, "length": 1, "offset": 0},
        5: {"start": 5, "length": 1, "offset": 0},
        6: {"start": 6, "length": 4, "offset": -6},
        10: {"start": 10, "length": 2, "offset": 0},
    }

    assert sut.update_mapped_ranges_mapped_ranges(mapped) == {
        9: {"start": 9, "length": 1, "offset": 0},
        6: {"start": 6, "length": 2, "offset": 0},
        4: {"start": 4, "length": 1, "offset": 0},
        5: {"start": 5, "length": 1, "offset": 0},
        0: {"start": 0, "length": 4, "offset": 0},
        10: {"start": 10, "length": 2, "offset": 0},
    }


def test_apply_map_to_source_ranges():
    case_A = {
        4: {"start": 4, "length": 2, "offset": 0},
        7: {"start": 7, "length": 3, "offset": 0},
    }
    case_B = {
        1: {"start": 1, "length": 4, "offset": 0},
        5: {"start": 5, "length": 7, "offset": 0},
    }
    mapping_line = "seed-to-soil map:\n0 6 4\n8 0 2\n6 2 2"

    assert sut.apply_map_to_source_ranges(case_A, mapping_line) == {
        4: {"start": 4, "length": 2, "offset": 0},
        1: {"start": 1, "length": 3, "offset": 0},
    }
    assert sut.apply_map_to_source_ranges(case_B, mapping_line) == {
        9: {"start": 9, "length": 1, "offset": 0},
        6: {"start": 6, "length": 2, "offset": 0},
        4: {"start": 4, "length": 1, "offset": 0},
        5: {"start": 5, "length": 1, "offset": 0},
        0: {"start": 0, "length": 4, "offset": 0},
        10: {"start": 10, "length": 2, "offset": 0},
    }


def test_part_2():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_2(lines) == 46
