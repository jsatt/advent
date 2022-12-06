from typing import Generator

def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def get_value(char: str) -> int:
    char_val = ord(char)
    if char_val >= 97:
        val = char_val - 96
    else:
        val = char_val - 38
    return val

def part_1(test: bool = False) -> int:
    val = 0
    for line in read_file(test):
        split = len(line) // 2
        c1 = set(line[:split])
        c2 = set(line[split:])
        common = c1.intersection(c2)
        val += get_value(common.pop())
    return val


def part_2(test: bool = False) -> int:
    lines = read_file(test)
    val = 0
    while True:
        try:
            e1 = set(next(lines))
            e2 = set(next(lines))
            e3 = set(next(lines))
        except StopIteration:
            break
        common = e1.intersection(e2).intersection(e3)
        val += get_value(common.pop())
    return val

