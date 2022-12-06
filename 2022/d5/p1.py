import re
from typing import Generator
from collections import defaultdict

def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.rstrip()

def parse_crates(stacks):
    stack_count = int(stacks.pop(-1)[-1])
    crate_stacks = [[] for _ in range(stack_count)]
    for line in stacks:
        crates = re.finditer(r'\[([A-Z])\]', line)
        for match in crates:
            stack = match.start() // 4
            crate_stacks[stack].insert(0, match.groups()[0])
    return crate_stacks


def part_1(test: bool = False) -> str:
    lines = read_file(test)
    crate_lines = []
    for line in lines:
        if line == '':
            break
        crate_lines.append(line)
    crates = parse_crates(crate_lines)

    for line in lines:
        _, count, _, source, _, dest = line.split(' ')
        for i in range(int(count)):
            crates[int(dest) - 1].append(crates[int(source) - 1].pop())

    return ''.join([s[-1] for s in crates])


def part_2(test: bool = False) -> str:
    lines = read_file(test)
    crate_lines = []
    for line in lines:
        if line == '':
            break
        crate_lines.append(line)
    crates = parse_crates(crate_lines)

    for line in lines:
        _, count, _, source, _, dest = line.split(' ')
        count = int(count)
        source = int(source) - 1
        dest = int(dest) - 1
        new_source = crates[source][:-count]
        moving = crates[source][-count:]
        crates[dest].extend(moving)
        crates[source] = new_source

    return ''.join([s[-1] for s in crates])
