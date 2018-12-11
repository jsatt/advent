import os
import re


def test_map_fabric():
    return run_map() == 107043


def run_map():
    regex = re.compile('#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)')
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        lines = [regex.search(l).groupdict() for l in f.read().splitlines() if l]
    fabric = map_fabric(lines)
    return len(filter(lambda x: x[1] == 'X', fabric.items()))


def map_fabric(inputs):
    fabric = {}

    for item in inputs:
        for xoff in range(int(item['w'])):
            for yoff in range(int(item['h'])):
                coords = (int(item['x']) + xoff, int(item['y']) + yoff)
                if coords not in fabric:
                    fabric[coords] = item['id']
                else:
                    fabric[coords] = 'X'

    return fabric
