from collections import defaultdict
import os
import re

## sample
INPUT_FILE = 'test_input.txt'
ANSWER = 57, 29


## Part 1
INPUT_FILE = 'input.txt'
ANSWER = 30635, 25094


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    grid = parse_map(lines)
    ys = [c[1] for c in grid.keys()]
    min_y, max_y = min(ys), max(ys)
    fill(grid, (500, min_y), min_y, max_y)
    render_map(grid)
    filled = len([c for c in grid.values() if c in '~'])
    flowed = len([c for c in grid.values() if c in '|'])
    return filled + flowed, filled


def parse_map(lines):
    grid = defaultdict(lambda: '.')
    pattern = re.compile('(.)=(\d+), (.)=(\d+)..(\d+)')
    for line in lines:
        loc_axis, loc_val, rng_axis, rng_start, rng_end = pattern.search(line).groups()
        loc_val = int(loc_val)
        rng_start = int(rng_start)
        rng_end = int(rng_end)
        for v in range(rng_start, rng_end + 1):
            if loc_axis == 'x':
                grid[loc_val, v] = '#'
            else:
                grid[v, loc_val] = '#'
    return grid


def render_map(grid):
    xs = [c[0] for c in grid.keys()]
    ys = [c[1] for c in grid.keys()]
    print('')
    print('')
    print('')
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            print(grid[x, y], end='')  # noqa
        print('')


def fill(grid, coord, min_y, max_y, direct='down'):
    if grid[coord] == '.':
        grid[coord] = '|'

    below = (coord[0], coord[1] + 1)
    left = (coord[0] - 1, coord[1])
    right = (coord[0] + 1, coord[1])

    if grid[below] != '#':
        if grid[below] not in '~|' and min_y <= coord[1] < max_y:
            fill(grid, below, min_y, max_y, 'down')
        if grid[below] != '~':
            return False

    left_filled = grid[left] == '#' or (grid[left] not in '~|' and fill(grid, left, min_y, max_y, 'left'))
    right_filled = grid[right] == '#' or (grid[right] not in '~|' and fill(grid, right, min_y, max_y, 'right'))

    if direct == 'down' and left_filled and right_filled:
        grid[coord] = '~'

        while grid[left] in '~|':
            grid[left] = '~'
            left = left[0] - 1, left[1]

        while grid[right] in '~|':
            grid[right] = '~'
            right = right[0] + 1, right[1]

    return (direct == 'left' and (left_filled or grid[left] == '#')) or (direct == 'right' and (right_filled or grid[right] == '#'))


class Overflow(Exception):
    pass
