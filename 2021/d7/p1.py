from collections import defaultdict
from typing import Tuple

import aiofiles


async def read_file(test: bool = False) -> str:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        return await f.read()


async def calculate_moves(test: bool = False) -> Tuple[int, int]:
    positions = [int(p) for p in (await read_file(test=test)).split(',')]
    max_pos = max(positions)
    fuel = defaultdict(int)
    for ppos in range(max_pos):
        for spos in positions:
            fuel[ppos] += abs(ppos - spos)
    min_pos = (None, None)
    for pos, posf in fuel.items():
        if min_pos[0] is None or posf < min_pos[0]:
            min_pos = posf, pos
    return min_pos


async def calculate_moves_gauss(test: bool = False) -> Tuple[int, int]:
    positions = [int(p) for p in (await read_file(test=test)).split(',')]
    max_pos = max(positions)
    fuel = defaultdict(int)
    for ppos in range(max_pos):
        for spos in positions:
            diff = abs(ppos - spos)
            fuel[ppos] += (diff * (diff + 1)) / 2
    min_pos = (None, None)
    for pos, posf in fuel.items():
        if min_pos[0] is None or posf < min_pos[0]:
            min_pos = posf, pos
    return min_pos


async def part_1(test: bool = False) -> int:
    fuel, pos = await calculate_moves(test=test)
    return fuel


async def part_2(test: bool = False) -> int:
    fuel, pos = await calculate_moves_gauss(test=test)
    return int(fuel)
