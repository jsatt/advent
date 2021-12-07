from collections import defaultdict
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


async def map_vents(include_diag: bool = True, test: bool = False) -> dict:
    vmap = defaultdict(int)
    async for line in read_file(test=test):
        (x1, y1), (x2, y2) = [map(int, c.split(',')) for c in line.split(' -> ')]
        if include_diag or x1 == x2 or y1 == y2:
            xs = 0 if x1 == x2 else 1 if x1 < x2 else -1
            ys = 0 if y1 == y2 else 1 if y1 < y2 else -1
            steps = max(abs(x1 - x2), abs(y1 - y2))
            for step in range(steps + 1):
                vmap[(x1 + (step * xs), y1 + (step * ys))] += 1
    return vmap


async def part_1(test: bool = False) -> int:
    vmap = await map_vents(include_diag=False, test=test)
    return len([v for v in vmap.values() if v >= 2])


async def part_2(test: bool = False) -> int:
    vmap = await map_vents(include_diag=True, test=test)
    return len([v for v in vmap.values() if v >= 2])
