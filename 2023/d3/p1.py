from collections import defaultdict
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


async def build_grid(rows):
    nums = {}
    symbols = {}
    ridx = 0
    async for row in (rows):
        width = len(row)
        cidx = 0
        while cidx < width:
            val = ''
            start = cidx
            if row[cidx][0].isdigit():
                while cidx < width and row[cidx][0] in '0123456789':
                    val += row[cidx][0]
                    cidx += 1
                for idx in range(len(val)):
                    nums[ridx, start] = val
            elif cidx < width and row[cidx][0] != '.':
                symbols[ridx, start] = row[cidx][0]
                cidx += 1
            else:
                cidx += 1
        ridx += 1
    return nums, symbols


def get_adjacent_locs(loc, num_len):
    min_col = loc[1] - 1
    max_col = loc[1] + num_len
    return [
        *[(loc[0] - 1, loc[1] - 1 + idx) for idx in range(num_len + 2)],
        (loc[0], min_col),
        (loc[0], max_col),
        *[(loc[0] + 1, loc[1] - 1 + idx) for idx in range(num_len + 2)],
    ]


def check_for_surrounding_symbol(symbols, loc, num_len):
    for idx in get_adjacent_locs(loc, num_len):
        if not symbols.get(idx, '0').isdigit():
            return True
    return False


async def part_1(test=False):
    rows = read_file(test=test)
    nums, symbols = await build_grid(rows)
    output = 0
    for loc in nums.keys():
        if check_for_surrounding_symbol(symbols, loc, len(nums[loc])):
            output += int(nums[loc])
    return output


def check_for_parts(nums, gears):
    gears = set(gears)
    gear_nums = defaultdict(list)
    for loc, val in nums.items():
        num_len = len(val)
        idxs = get_adjacent_locs(loc, num_len)
        for l in gears.intersection(idxs):
            gear_nums[l].append(int(val))
    return sum([x[0] * x[1] for x in gear_nums.values() if len(x) == 2])


async def part_2(test=False):
    rows = read_file(test=test)
    nums, symbols = await build_grid(rows)
    output = 0
    gears = [loc for loc, val in symbols.items() if val == '*']
    output += check_for_parts(nums, gears)
    return output
