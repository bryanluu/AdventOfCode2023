import Day03 as sut

EXAMPLE_FILENAME = "example.txt"

def test_part_1():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_1(lines) == 4361

def test_part_2():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_2(lines) == 467835

def test_engine_schematic():
    with open(EXAMPLE_FILENAME, "r") as file:
        raw_schematic = file.read().strip()

    schematic = sut.EngineSchematic(raw_schematic)

    assert schematic.grid.shape == (10, 10)
    assert schematic.numbers[0]["value"] == 467
    assert schematic.get_neighbor_positions(schematic.numbers[0]) == [(0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]
    assert schematic.gears[(1, 3)] == [467, 35]
    assert schematic.gear_ratios[(1, 3)] == 467 * 35
    assert len(schematic.numbers) == 10
    assert len(schematic.part_numbers) == 8
    assert len(schematic.gears) == 2
