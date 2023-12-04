from functools import reduce
from operator import mul
from typing import AsyncGenerator

import aiofiles


async def read_file(test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()

async def part_1(test=False):
    max_count = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }
    output = 0
    async for game in read_file(test=test):
        title, plays = game.split(': ')
        possible = True
        for pull in plays.split('; '):
            for clr_cnt in pull.split(', '):
                count, color = clr_cnt.split(' ')
                if int(count) > max_count[color]:
                    possible = False
                    break
            if not possible:
                break
        if possible:
            output += int(title.split(' ')[1])
    return output


async def part_2(test=False):
    output = 0
    async for game in read_file(test=test):
        title, plays = game.split(': ')
        max_count = {'red': 0, 'blue': 0, 'green': 0}
        for pull in plays.split('; '):
            for clr_cnt in pull.split(', '):
                count, color = clr_cnt.split(' ')
                count = int(count)
                if count > max_count[color]:
                    max_count[color] = count
        output += reduce(mul, max_count.values())
    return output
