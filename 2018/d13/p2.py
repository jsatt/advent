import os
from collections import deque, defaultdict
from itertools import chain

## sample
INPUT_FILE = 'test_input2.txt'
ANSWER = (6, 4)

## Part 2
INPUT_FILE = 'input.txt'
ANSWER = (50, 100)


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        tracks, carts = parse_map(f.read().splitlines())

    # render_grid(tracks, carts)
    while carts:
        carts = tick(tracks, carts)
        if len(carts) == 1:
            return carts[0].x, carts[0].y

    # return tracks, carts


def parse_map(lines):
    tracks = []
    carts = []
    for yidx, line in enumerate(lines):
        row = []
        tracks.append(row)
        for xidx, char in enumerate(line):
            if char in '<>':
                track = '-'
            elif char in '^v':
                track = '|'
            else:
                track = char

            row.append(track)

            if char in '<>v^':
                carts.append(Cart(xidx, yidx, char))
    return tracks, carts


def render_grid(tracks, carts):
    cart_coords = defaultdict(list)
    for cart in carts:
        cart_coords[cart.x, cart.y].append(cart)

    for yidx, row in enumerate(tracks):
        for xidx, cell in enumerate(row):
            cart = cart_coords.get((xidx, yidx))
            if not cart:
                print(cell, end='')
            elif len(cart) > 1:
                print('X', end='')
            else:
                print(cart[0].direction, end='')
        print('')


def tick(tracks, carts):
    sorted_carts = sorted(carts, key=lambda c: (c.y, c.x))
    for cart in sorted_carts:
        cart.move()
        cart.update_direction(tracks[cart.y][cart.x])
        for other_cart in sorted_carts:
            if other_cart is not cart and other_cart.x == cart.x and cart.y == other_cart.y:
                other_cart.crashed = True
                cart.crashed = True
    return [c for c in sorted_carts if not c.crashed]


class Cart:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.set_direction(direction)
        self.crashed = False
        self.intersection_cycle = deque([1, 0, -1])

    def set_direction(self, direction):
        self.directions = deque(['<', '^', '>', 'v'])
        self.directions.rotate(-self.directions.index(direction))

    @property
    def direction(self):
        return self.directions[0]

    def move(self):
        if self.direction == '<':
            self.x -= 1
        elif self.direction == '>':
            self.x += 1
        elif self.direction == 'v':
            self.y += 1
        elif self.direction == '^':
            self.y -= 1

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
