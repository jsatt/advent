from typing import Generator

import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l

LENGTH_MAP = {  # number of segments for each digit
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}

COMMON_SEG_MAP = {  # count of shared segments with 1, 4, 7, 8
    '2336': 0,  # ie. 1: 2 segs, 4: 3 segs, 7: 3 segs, 8: 6 segs
    '1225': 2,
    '2335': 3,
    '1325': 5,
    '1326': 6,
    '2436': 9
}

def detect_wiring(patterns) -> dict:
    digit_map = {}
    unmatched = []
    for pattern in patterns:
        key = set(pattern)
        if (len_key := len(key)) in LENGTH_MAP:
            digit_map[LENGTH_MAP[len_key]] = key
        else:
            unmatched.append(key)
    for pattern in unmatched:
        key = []
        for known in [1, 4, 7, 8]:
            kkey = digit_map[known]
            key.append(str(len(kkey & pattern)))
        lkey = ''.join(key)
        digit_map[COMMON_SEG_MAP[lkey]] = pattern
    return {''.join(sorted(v)): str(k) for k, v in digit_map.items()}


def decode_output(digit_map, output) -> int:
    result = []
    for val in output:
        key = ''.join(sorted(val))
        result.append(digit_map[key])
    return int(''.join(result))


async def part_1(test: bool = False) -> int:
    return len([
        d
        async for l in read_file(test=test)
        for d in l.split('|')[1].split()
        if len(d) in LENGTH_MAP
    ])


async def part_2(test: bool = False):
    result = 0
    async for line in read_file(test=test):
        sample, output = line.split('|')
        patterns = sample.split()
        digit_map = detect_wiring(patterns)
        result += decode_output(digit_map, output.split())
    return result
