from typing import Generator, Iterable
from operator import mul

def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def part_1(test: bool = False) -> int:
    visible_count = 0
    lines = [
        [int(c) for c in l]
        for l in read_file(test)
    ]
    row_count = len(lines)
    col_count = len(lines[0])
    for ridx, row in enumerate(lines):
        for cidx, tree in enumerate(row):
            if not (0 < ridx < row_count - 1 and 0 < cidx < col_count - 1) or (
                (tree > max(row[:cidx]) or
                 tree > max(row[cidx + 1:])or
                 tree > max([lines[i][cidx] for i in range(ridx)]) or
                 tree > max([lines[i][cidx] for i in range(ridx + 1, row_count)]))):
                    visible_count += 1

    return visible_count


def count_visible(neighbors, tree):
    count = 0
    for neighbor in neighbors:
        if neighbor <= tree:
            count += 1
        if neighbor >= tree:
            break
    return count


def part_2(test: bool = False) -> int:
    max_scenic_score = 0
    lines = [
        [int(c) for c in l]
        for l in read_file(test)
    ]
    row_count = len(lines)
    col_count = len(lines[0])
    for ridx, row in enumerate(lines):
        for cidx, tree in enumerate(row):
            scenic_score = (
                count_visible(reversed(row[:cidx]), tree) *
                count_visible(row[cidx + 1:], tree) *
                count_visible(reversed([lines[i][cidx] for i in range(ridx)]), tree) *
                count_visible([lines[i][cidx] for i in range(ridx + 1, row_count)], tree)
            )
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    return max_scenic_score
