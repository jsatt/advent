from itertools import product
import re


def read_file(test: bool = False):
    if test:
        file_name = 'test_input.txt'
        # file_name = 'sample_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def count_groups(row):
    counts = []
    run = 0
    for char in row:
        if char == '#':
            run += 1
        elif run:
            counts.append(run)
            run = 0
    if run:
        counts.append(run)
    return counts


def find_possible_combinations(_len):
    return [''.join(x) for x in product('.#', repeat=_len)]


def part_1(test=False):
    output = 0
    for line in read_file(test=test):
        row, counts = line.split()
        groups = list(map(int, counts.split(',')))
        sub_groups = re.findall(r'\?+', row)
        match_count = 0
        for g in product(*[find_possible_combinations(len(sg)) for sg in sub_groups]):
            val = row
            for r in g:
                val = re.sub(r'\?+', r, val, count=1)
            if count_groups(val) == groups:
                match_count += 1

        output += match_count
    return output
