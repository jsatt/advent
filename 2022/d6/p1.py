from collections import Counter
from typing import Generator

def read_file(test: bool = False) -> str:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        return f.readline().rstrip()


def find_distinct(stream, count):
    for idx, char in enumerate(stream):
        if idx >= count:
            substr = stream[idx - count:idx]
            counts = Counter(substr).most_common()
            if counts and counts[0][1] == 1:
                return idx
    return -1


def part_1(test: bool = False) -> int:
    stream = read_file(test)
    # for idx, char in enumerate(stream):
    #     if idx >= 4:
    #         substr = stream[idx-4:idx]
    #         counts = Counter(substr).most_common()
    #         if counts and counts[0][1] == 1:
    #             return idx
    return find_distinct(stream, 4)


def part_2(test: bool = False) -> int:
    stream = read_file(test)
    return find_distinct(stream, 14)
