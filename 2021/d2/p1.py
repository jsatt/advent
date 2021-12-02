from typing import Generator, Sequence
import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l

async def calculate_location(test: bool = False) -> Sequence[int]:
    location = [0, 0]

    async for line in read_file(test=test):
        direct, dist = line.split(' ')
        dist = int(dist)
        if direct == 'forward':
            location[0] += dist
        elif direct == 'up':
            location[1] -= dist
        else:
            location[1] += dist
    return location


async def part_1(test: bool = False) -> int:
    location = await calculate_location(test=test)
    return location[0] * location[1]
