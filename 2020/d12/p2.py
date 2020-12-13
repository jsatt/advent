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


def move_waypoint(location, direction, val):
    if direction == 'N':
        location[0] += val
    elif direction == 'S':
        location[0] -= val
    elif direction == 'E':
        location[1] += val
    elif direction == 'W':
        location[1] -= val


def rotate_waypoint(location, direction, val):
    for _ in range(val):
        if direction == 'R':
            location[0], location[1] = -location[1], location[0]
        elif direction == 'L':
            location[0], location[1] = location[1], -location[0]


def walk_actions(actions):
    boat_location = [0, 0]
    waypoint_location = [1, 10]
    for action, val in actions:
        if action in 'NESW':
            move_waypoint(waypoint_location, action, val)
        elif action == 'F':
            boat_location[0] += waypoint_location[0] * val
            boat_location[1] += waypoint_location[1] * val
        elif action in 'LR':
            turns = val // 90
            rotate_waypoint(waypoint_location, action, turns)
        print(f'{action}{val} - B{boat_location} - W{waypoint_location}')
    return boat_location


def p2():
    actions = read_input()
    location = walk_actions(actions)
    return sum(map(abs, location))

