import os
import re


# INPUT_FILE = 'test_input.txt'
# ANSWER = 3
INPUT_FILE = 'input.txt'
ANSWER = 10595
# part 1 displays "JLPZFJRH"


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    points = parse_points(lines)
    timestamp = find_small_bounds(points)
    render_points(points, timestamp)
    return seconds


class Point:
    def __init__(self, x, y, xv, yv):
        self.start_x = x
        self.start_y = y
        self.x_velocity = xv
        self.y_velocity = yv

    def calc_move(self, seconds):
        return (
            self.start_x + (seconds * self.x_velocity),
            self.start_y + (seconds * self.y_velocity)
        )

    def __repr__(self):
        return '<{}: {}, {}; moving {}, {}>'.format(
            self.__class__.__name__, self.start_x, self.start_y,
            self.x_velocity, self.y_velocity)


def parse_points(lines):
    regex = re.compile('position=<(.*)> velocity=<(.*)>')
    points = []
    for line in lines:
        pos, velocity = regex.search(line).groups()
        x, y = (int(c.strip()) for c in pos.split(','))
        xv, yv = (int(v.strip()) for v in velocity.split(','))
        points.append(Point(x, y, xv, yv))
    return points


def find_small_bounds(points):
    seconds = 0
    min_x_range = 0
    min_y_range = 0
    x_range = 0
    y_range = 0
    while True:
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for point in points:
            x, y = point.calc_move(seconds)
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        x_range = max_x - min_x
        y_range = max_y - min_y
        if seconds == 0:
            min_x_range = x_range
            min_y_range = y_range
        elif x_range > min_x_range or y_range > min_y_range:
            break
        else:
            min_x_range = min(min_x_range, x_range)
            min_y_range = min(min_y_range, y_range)
        seconds += 1

    return seconds - 1


def render_points(points, seconds):
    coords = []
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for point in points:
        x, y = pos = point.calc_move(seconds)
        coords.append(pos)
        if x < min_x:
            min_x = x
        if x > max_x:
            max_x = x
        if y < min_y:
            min_y = y
        if y > max_y:
            max_y = y
    print('Seconds: {}'.format(seconds))
    for iy in range(min_y, max_y + 1):
        for ix in range(min_x, max_x + 1):
            if (ix, iy) in coords:
                print('*', end='')
            else:
                print('.', end='')
        print('')
    return min_x, max_x, min_y, max_y
