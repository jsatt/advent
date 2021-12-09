from functools import reduce
from operator import mul
from typing import Generator, List, Optional, Tuple

import aiofiles


async def aenumerate(asequence):
    idx = 0
    async for item in asequence:
        yield (idx, item)
        idx += 1


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l


async def build_map(test: bool = False) -> dict:
    heightmap = {}
    async for ridx, line in aenumerate(read_file(test=test)):
        for cidx, cell in enumerate(line.strip()):
            heightmap[(ridx, cidx)] = int(cell)
    return heightmap


def calc_lower(
        heightmap: dict, pos: Tuple[int, int], find_basin: bool = False,
        current_basin: Optional[list] = None) -> List[Tuple[int, int]]:
    if not current_basin:
        current_basin = []
    if pos in heightmap and pos not in current_basin:
        x, y = pos
        val = heightmap[pos]
        up = (x - 1, y)
        down = (x + 1, y)
        left = (x, y - 1)
        right =(x, y + 1)
        is_above_val = lambda x: True if x in current_basin else heightmap.get(x, 9) >= val
        if (val < 9 and all(map(is_above_val, [up, down, left, right]))):
            current_basin.append(pos)
            if find_basin:
                calc_lower(heightmap, up, find_basin=find_basin, current_basin=current_basin)
                calc_lower(heightmap, down, find_basin=find_basin, current_basin=current_basin)
                calc_lower(heightmap, left, find_basin=find_basin, current_basin=current_basin)
                calc_lower(heightmap, right, find_basin=find_basin, current_basin=current_basin)
    return current_basin


def walk_map(heightmap: dict, find_basin: bool = False) -> List[List[Tuple[int, int]]]:
    basins = []
    for pos in heightmap.keys():
        basin = calc_lower(heightmap, pos, find_basin=find_basin)
        if basin:
            basins.append(basin)
    return basins


async def part_1(test: bool = False) -> int:
    heightmap = await build_map(test=test)
    lowspots = walk_map(heightmap)
    return sum([heightmap[p[0]] + 1 for p in lowspots])


async def part_2(test: bool = False) -> int:
    heightmap = await build_map(test=test)
    basins = walk_map(heightmap, find_basin=True,)
    basin_sizes = [len(b) for b in basins]
    basin_sizes.sort()
    return reduce(mul, basin_sizes[-3:])
