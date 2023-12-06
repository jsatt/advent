import sys
from operator import itemgetter
from collections import defaultdict


def read_file(test: bool = False):
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()

map_order = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location',
]

def parse_maps(lines):
    maps = defaultdict(list)

    cur_map = ''
    for line in lines:
        if not line:
            continue

        parts = line.split()

        if parts[-1] == 'map:':
            cur_map = parts[0]
        else:
            maps[cur_map].append(tuple(int(p) for p in parts))
    return maps

def find_min_loc(seeds, maps):
    min_loc = None
    for seed in seeds:
        id = seed
        for map in map_order:
            for dst, src, ln in maps[map]:
                if src <= id <= src + ln:
                    id2 = dst + (id - src)
                    id = id2
                    break

        if min_loc is None or id < min_loc:
            min_loc = id
    return min_loc


def part_1(test=False):
    lines = read_file(test=test)
    seeds = [int(s) for s in next(lines).split()[1:]]
    maps = parse_maps(lines)
    return find_min_loc(seeds, maps)
