import Day03 as sut

EXAMPLE_FILENAME = "example.txt"

def test_part_1():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_1(lines) == 4361

def test_engine_schematic():
    with open(EXAMPLE_FILENAME, "r") as file:
        raw_schematic = file.read().strip()

    schematic = sut.EngineSchematic(raw_schematic)

    assert schematic.grid.shape == (10, 10)
    assert len(schematic.numbers) == 10
    assert len(schematic.part_numbers) == 8
