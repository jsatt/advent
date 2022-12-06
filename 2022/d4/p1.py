from typing import Generator, List, Tuple

def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()

def get_ranges(line) -> Tuple[List[int], List[int]]:
    e1, e2 = line.split(',')
    r1 = [int(i) for i in e1.split('-')]
    r2 = [int(i) for i in e2.split('-')]
    return r1, r2


def part_1(test: bool = False) -> int:
    val = 0
    for line in read_file(test):
        r1, r2 = get_ranges(line)

        if (r1[0] <= r2[0] and r1[1] >= r2[1]) or (r2[0] <= r1[0] and r2[1] >= r1[1]):
            val += 1
    return val

def part_2(test: bool = False) -> int:
    val = 0
    for line in read_file(test):
        r1, r2 = get_ranges(line)
        if (r1[0] <= r2[0] <= r1[1] or r1[0]<= r2[1] <= r1[1]) or (r2[0] <= r1[0] <= r2[1] or r2[0]<= r1[1] <= r2[1]):
            val += 1
    return val
