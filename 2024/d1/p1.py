from collections import defaultdict
from collections.abc import AsyncGenerator

import aiofiles


async def read_file(test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()


async def part_1(test: bool = False) -> int:
    list1 = []
    list2 = []

    async for line in read_file(test=test):
        l1, l2 = line.split()
        list1.append(int(l1))
        list2.append(int(l2))

    list1.sort()
    list2.sort()

    return sum(abs(l1 - l2) for l1, l2 in zip(list1, list2))


async def part_2(test: bool = False) -> int:
    list1 = []
    sim_counts = defaultdict(int)

    async for line in read_file(test=test):
        l1, l2 = line.split()
        list1.append(int(l1))
        sim_counts[int(l2)] += 1

    return sum(l * sim_counts[l] for l in list1)
