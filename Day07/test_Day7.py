import Day07 as sut

EXAMPLE_FILENAME = "example.txt"

def test_card_value():
    assert sut.card_value("2") == 0
    assert sut.card_value("3") == 1
    assert sut.card_value("4") == 2
    assert sut.card_value("5") == 3
    assert sut.card_value("6") == 4
    assert sut.card_value("7") == 5
    assert sut.card_value("8") == 6
    assert sut.card_value("9") == 7
    assert sut.card_value("T") == 8
    assert sut.card_value("J") == 9
    assert sut.card_value("Q") == 10
    assert sut.card_value("K") == 11
    assert sut.card_value("A") == 12

def test_hand_value():
    assert sut.hand_value("T6") == 8*13+4

def test_group_hand():
    hand = [1, 1, 1, 1, 1]
    assert sut.group_hand(hand) == 6

    hand = [1, 1, 1, 1, 2]
    assert sut.group_hand(hand) == 5

    hand = [1, 1, 1, 2, 2]
    assert sut.group_hand(hand) == 4

    hand = [1, 1, 1, 2, 3]
    assert sut.group_hand(hand) == 3

    hand = [1, 1, 2, 2, 3]
    assert sut.group_hand(hand) == 2

    hand = [1, 2, 2, 3, 4]
    assert sut.group_hand(hand) == 1

    hand = [1, 2, 3, 4, 5]
    assert sut.group_hand(hand) == 0

def test_parse_line():
    line = "hand 123"
    hand, bid = sut.parse_line(line)
    assert hand == "hand"
    assert bid == 123

def test_part_1():
    lines = []
    with open(EXAMPLE_FILENAME, "r") as file:
        lines = file.readlines()

    assert sut.solve_part_1(lines) == 6440
