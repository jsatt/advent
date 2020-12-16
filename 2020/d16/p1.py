from math import prod
from collections import defaultdict
import re

# FILENAME = 'test_input_1.txt'
FILENAME = 'test_input_2.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return f.readlines()

def parse_input(lines):
    fields = {}
    own_ticket = []
    other_tickets = []
    section = 'fields'
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        elif line == 'your ticket:':
            section = 'own'
            continue
        elif line == 'nearby tickets:':
            section = 'nearby'
            continue

        if section == 'fields':
            field, ranges = parse_fields(line)
            fields[field] = ranges
        elif section == 'own':
            own_ticket = [int(x) for x in line.split(',')]
        elif section == 'nearby':
            other_tickets.append([int(x) for x in line.split(',')])
    return fields, own_ticket, other_tickets


def parse_fields(line):
    match = re.match(r'([\w\s]+): (?:(\d+)\-(\d+)) or (?:(\d+)\-(\d+))', line)
    field, r1_min, r1_max, r2_min, r2_max = match.groups()
    return field, [(int(r1_min), int(r1_max)), (int(r2_min), int(r2_max))]


def p1():
    lines = read_input()
    fields, _, tickets = parse_input(lines)
    ranges = [x for f in fields.values() for x in f]
    invalids = [x for t in tickets for x in t if not any([r1 <= x <= r2 for r1, r2 in ranges])]
    return sum(invalids)

def is_valid(ticket, ranges):
    for val in ticket:
        if not any([r1 <= val <= r2 for r1, r2 in ranges]):
            return False
    return True

def lock_field(field, keep_idx, possibles, taken):
    taken.append(field)
    for idx, pos_list in possibles.items():
        if idx == keep_idx:
            continue
        if len(pos_list) > 1 and field in pos_list:
            pos_list.pop(pos_list.index(field))
            if len(pos_list) == 1:
                lock_field(pos_list[0], idx, possibles, taken)


def find_fields(groups, fields):
    possibles = defaultdict(list)
    taken = []
    for gidx, group in enumerate(groups):
        pos_list = possibles[gidx]
        for field, ranges in fields.items():
            if field not in taken:
                if all([ranges[0][0] <= x <= ranges[0][1] or
                        ranges[1][0] <= x <= ranges[1][1]
                        for x in group]):
                    pos_list.append(field)
        if len(pos_list) == 1:
            lock_field(pos_list[0], gidx, possibles, taken)

    return dict((f[0], i) for i, f in possibles.items())


def p2():
    lines = read_input()
    fields, own, tickets = parse_input(lines)
    ranges = [x for f in fields.values() for x in f]
    valids = [t for t in [own] + tickets if is_valid(t, ranges)]
    groups = list(zip(*valids))
    mapping = find_fields(groups, fields)
    my_ticket = dict((f, own[i]) for f, i in mapping.items())
    return prod(v for k, v in my_ticket.items() if k.startswith('departure'))
