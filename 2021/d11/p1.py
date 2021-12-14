from typing import Generator, Tuple

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
    octomap = {}
    async for ridx, line in aenumerate(read_file(test=test)):
        for cidx, cell in enumerate(line.strip()):
            octomap[(ridx, cidx)] = int(cell)
    return octomap


def incr_octo(pos: Tuple[int, int], octomap: dict, flashed: set):
    if pos in octomap.keys() and pos not in flashed:
        octomap[pos] += 1
        if octomap[pos] > 9:
            flashed.add(pos)
            octomap[pos] = 0
            for neightbor in [
                (pos[0]-1, pos[1]-1),
                (pos[0]-1, pos[1]),
                (pos[0]-1, pos[1]+1),
                (pos[0], pos[1]-1),
                (pos[0], pos[1]+1),
                (pos[0]+1, pos[1]-1),
                (pos[0]+1, pos[1]),
                (pos[0]+1, pos[1]+1),
            ]:
                incr_octo(neightbor, octomap, flashed)


async def part_1(cycles: int = 100, test: bool = False) -> int:
    octomap = await build_map(test=test)
    flashes = 0
    for _ in range(cycles):
        flashed = set()
        for pos in octomap:
            incr_octo(pos, octomap, flashed)
        flashes += len(flashed)
    return flashes


async def part_2(test: bool = False) -> int:
    octomap = await build_map(test=test)
    flashes = 0
    cycle = 0
    while flashes < 100:
        flashed = set()
        for pos in octomap:
            incr_octo(pos, octomap, flashed)
        flashes = len(flashed)
        cycle += 1
    return cycle
