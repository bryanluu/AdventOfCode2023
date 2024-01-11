#!/bin/python3
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

import functools as ft
from collections import Counter

CARD_ORDER = "23456789TJQKA"

def card_value(card):
    """Return the value of a card"""
    return CARD_ORDER.index(card[0])

def hand_value(hand):
    """Return the value of a hand"""
    value = 0
    for pos, card in enumerate(reversed(hand)):
        value += card_value(card) * len(CARD_ORDER)**pos
    return value

def group_hand(hand):
    """Determine the group the hand belongs to"""
    # Count the number of each card, sorted by count
    card_count = Counter(hand)
    counts = "".join(map(str, sorted(card_count.values(), reverse=True)))
    # Group 6: 5 of a kind
    if counts == "5":
        return 6
    # Group 5: 4 of a kind
    elif counts == "41":
        return 5
    # Group 4: Full house
    elif counts == "32":
        return 4
    # Group 3: 3 of a kind
    elif counts == "311":
        return 3
    # Group 2: 2 pairs
    elif counts == "221":
        return 2
    # Group 1: 1 pair
    elif counts == "2111":
        return 1
    # Group 0: High card
    else:
        return 0

def hand_key(hand):
    """Key function used to compare hands according to described rules"""
    return hand_value(hand) + group_hand(hand) * len(CARD_ORDER)**5

def parse_line(line):
    hand, bid_str = line.split(" ")
    bid = int(bid_str)
    return hand, bid

def solve_part_1(lines):
    bids = { hand: bid for hand, bid in map(parse_line, lines) }
    sorted_hands = sorted(bids.keys(), key=hand_key)
    result = ft.reduce(lambda acc, pair: acc + pair[0] * bids[pair[1]],
                        zip(range(1, len(sorted_hands)+1), sorted_hands),
                        0)
    return result

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
