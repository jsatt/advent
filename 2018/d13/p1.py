import os
from collections import deque, defaultdict
from itertools import chain

## sample
# INPUT_FILE = 'test_input.txt'
# ANSWER = (7, 3)

## Part 1
INPUT_FILE = 'input.txt'
ANSWER = (50, 54)

def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        grid = Grid.from_map(f.read().splitlines())

    # grid.render_grid()
    while True:
        grid.tick()
        # grid.render_grid()
        crashes = grid.get_crashes()
        if crashes:
            return crashes[0][0]

    return grid

class Grid:
    def __init__(self, cells, carts):
        self.cells = cells
        self.carts = carts

    @classmethod
    def from_map(cls, lines):
        cells = []
        carts = {}
        for yidx, line in enumerate(lines):
            row = []
            cells.append(row)
            for xidx, char in enumerate(line):
                if char in '<>':
                    track = '-'
                elif char in '^v':
                    track = '|'
                else:
                    track = char

                row.append(track)

                if char in '<>v^':
                    cart = Cart(char)
                    carts[(xidx, yidx)] = [cart]
        return cls(cells, carts)

    def get_crashes(self):
        return list(filter(lambda c: len(c[1]) > 1, self.carts.items()))

    def tick(self):
        moved_carts = defaultdict(list)
        for yidx, row in enumerate(self.cells):
            for xidx, cell in enumerate(row):
                carts = self.carts.get((xidx, yidx))
                if carts:
                    cart = carts[0]
                    if cart.direction == '<':
                        new_coords = (xidx - 1, yidx)
                    elif cart.direction == '>':
                        new_coords = (xidx + 1, yidx)
                    elif cart.direction == '^':
                        new_coords = (xidx, yidx - 1)
                    elif cart.direction == 'v':
                        new_coords = (xidx, yidx + 1)

                    moved_carts[new_coords].append(cart)
                    cart.update_direction(self.cells[new_coords[1]][new_coords[0]])
                    # print('moving cart {} from {} to {}'.format(cart.direction, (xidx, yidx), new_coords))
        self.carts = moved_carts

    def render_grid(self):
        for yidx, row in enumerate(self.cells):
            for xidx, cell in enumerate(row):
                carts = self.carts.get((xidx, yidx))
                if not carts:
                    print(cell, end='')
                elif len(carts) > 1:
                    print('X', end='')
                else:
                    print(carts[0].direction, end='')
            print('')


class Cart:
    def __init__(self, direction):
        self.set_direction(direction)
        self.intersection_cycle = deque([1, 0, -1])

    def set_direction(self, direction):
        self.directions = deque(['<', '^', '>', 'v'])
        self.directions.rotate(-self.directions.index(direction))

    @property
    def direction(self):
        return self.directions[0]

    def update_direction(self, track):
        if track == '+':
            self.directions.rotate(self.intersection_cycle[0])
            self.intersection_cycle.rotate(-1)
        elif track == '\\':
            if self.direction in '<>':
                self.directions.rotate(-1)
            elif self.direction in 'v^':
                self.directions.rotate(1)
        elif track == '/':
            if self.direction in '<>':
                self.directions.rotate(1)
            elif self.direction in 'v^':
                self.directions.rotate(-1)
        return self.direction

    def __repr__(self):
        return self.direction
