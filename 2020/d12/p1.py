import re
from collections import deque

# FILENAME = 'test_input.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return [parse_line(l) for l in f.readlines()]


def parse_line(line):
    action, val = re.match('(\w)(\d+)', line).groups()
    return action, int(val)


def move_boat(location, direction, val):
    if direction == 'N':
        location[0] += val
    elif direction == 'S':
        location[0] -= val
    elif direction == 'E':
        location[1] += val
    elif direction == 'W':
        location[1] -= val


def walk_actions(actions):
    location = [0, 0]
    direction = deque(['E', 'S', 'W', 'N'])
    for action, val in actions:
        if action in ['N', 'E', 'S', 'W']:
            move_boat(location, action, val)
        elif action == 'F':
            move_boat(location, direction[0], val)
        elif action == 'R':
            turns = val // 90
            direction.rotate(-turns)
        elif action == 'L':
            turns = val // 90
            direction.rotate(turns)
    return location


def p1():
    actions = read_input()
    location = walk_actions(actions)
    return sum(map(abs, location))
