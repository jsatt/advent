import re
from typing import AsyncGenerator

import aiofiles


async def read_file(part: int, test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        if part == 2:
            file_name = 'test_input_2.txt'
        else:
            file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()


async def part_1(test: bool = False) -> int:
    total = 0
    async for line in read_file(part=1, test=test):
        digits = re.sub('[^\d]', '', line)
        if digits:
            total += int(digits[0] + digits[-1])
    return total


def normalize_numbers(line: str) -> str:
    num_map = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
               'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    for name, val in num_map.items():
        # This is a stupid solution
        line = line.replace(name, f'{name[:1]}{val}{name[1:]}')
    return line


async def part_2(test: bool = False) -> int:
    total = 0
    async for line in read_file(part=2, test=test):
        normalized = normalize_numbers(line)
        digits = re.sub(r'[^\d]', '', normalized)
        if digits:
            total += int(digits[0] + digits[-1])
    return total
