import os

## sample
GENERATIONS = 100000
INPUT_FILE = 'test_input.txt'
ANSWER = 325

## Part 1
# GENERATIONS = 20
# INPUT_FILE = 'input.txt'
# ANSWER = 3337


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        state = f.readline().strip().split(': ')[1]
        f.readline()
        rules = parse_rule(f.read().splitlines())

    total_offset = 0
    for x in range(1, GENERATIONS + 1):
        state, offset = run_generation(state, rules)
        total_offset += offset

    return count_pots(state, total_offset)


def parse_rule(lines):
    rules = {}
    for line in lines:
        match, result = line.split(' => ')
        rules[match] = result
    return rules


def run_generation(state, rules):
    offset = -3
    new_state = ''
    state = '...' + state
    for idx in range(len(state) + 2):
        if idx <= 2:
            block = ('.' * (2 - idx)) + state[:idx + 3]
        elif idx > len(state) - 3:
            block = state[idx - 2:] + ('.' * (3 - (len(state) - idx)))
        else:
            block = state[idx - 2:idx + 3]
        new_state += rules.get(block, '.')
    while new_state[-1] == '.':
        new_state = new_state[:-1]
    while new_state[0] == '.':
        offset += 1
        new_state = new_state[1:]
    return new_state, offset


def count_pots(state, offset):
    pot_sum = 0
    for idx, plant in enumerate(state):
        if plant == '#':
            pot_sum += idx + offset
    return pot_sum

