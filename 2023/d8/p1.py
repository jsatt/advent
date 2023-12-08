from itertools import cycle
import re
from math import lcm


def read_file(test=None):
    if test:
        file_name = f'test_input_{test}.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def parse_nodes(lines):
    dirs = next(lines)
    next(lines)

    nodes = {
        g[0]: (g[1], g[2])
        for line in lines
        if (g := re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', line).groups())
    }
    return nodes, dirs


def walk_nodes(start_node, nodes, dirs, end_test):
    steps = 0
    curr_node = start_node
    for d in cycle(dirs):
        node = nodes[curr_node]

        if d == 'L':
            curr_node = node[0]
        else:
            curr_node = node[1]

        steps += 1

        if end_test(curr_node):
            break

    return steps


def part_1(test=None):
    lines = read_file(test=test)
    nodes, dirs = parse_nodes(lines)
    return walk_nodes('AAA', nodes, dirs, lambda n: n == 'ZZZ')


def part_2(test=None):
    lines = read_file(test=test)
    nodes, dirs = parse_nodes(lines)
    step_counts = []
    for curr_node in nodes:
        if curr_node.endswith('A'):
            step_counts.append(walk_nodes(curr_node, nodes, dirs, lambda n: n.endswith('Z')))
    return lcm(*step_counts)
