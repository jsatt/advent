import os
from collections import deque

## sample
GENERATIONS = 20
INPUT_FILE = 'test_input.txt'
ANSWER = 325

## Part 1
# GENERATIONS = 20
# INPUT_FILE = 'input.txt'
# ANSWER = 3337

## Part 2
# GENERATIONS = 50000000000
# INPUT_FILE = 'input.txt'
# ANSWER = 3337


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        state = deque(f.readline().strip().split(': ')[1])
        f.readline()
        rules = parse_rule(f.read().splitlines())
    total_offset = 0
    for x in range(1, GENERATIONS + 1):
        state, offset = run_generation(state, rules)
        total_offset += offset
        if x % 100000 == 0:
            print(x)

    return count_pots(state, total_offset)


def parse_rule(lines):
    rules = {}
    for line in lines:
        match, result = line.split(' => ')
        rules[match] = result
    return rules


def run_generation(state, rules):
    offset = -2
    new_state = deque()
    block = deque('.....')
    state.extend('....')
    for idx in range(len(state)):
        block.popleft()
        block.append(state.popleft())
        new_state.append(rules.get(''.join(block), '.'))
    while new_state[-1] == '.':
        new_state.pop()
    while new_state[0] == '.':
        offset += 1
        new_state.popleft()
    return new_state, offset


def count_pots(state, offset):
    pot_sum = 0
    for idx, plant in enumerate(state):
        if plant == '#':
            pot_sum += idx + offset
    return pot_sum

