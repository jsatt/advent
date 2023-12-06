from functools import reduce
from operator import mul


def read_file(test: bool = False):
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def find_wins(time, max_dist):
    for t in range(1, time + 1):
        dist = t * (time - t)
        if dist > max_dist:
            return (time - t) - t + 1



def part_1(test=False):
    lines = read_file(test=test)
    races = zip(map(int, next(lines).split()[1:]), map(int, next(lines).split()[1:]))

    wins = []
    for time, max_dist in races:
        wins.append(find_wins(time, max_dist))
    return reduce(mul, wins)


def part_2(test=False):
    lines = read_file(test=test)
    time = int(''.join(next(lines).split()[1:]))
    max_dist = int(''.join(next(lines).split()[1:]))
    return find_wins(time, max_dist)
