from typing import AsyncGenerator, Iterable

import aiofiles

async def read_file(test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()

async def get_elf_ttls(test: bool = False) -> Iterable:
    elves = []
    elf_ttl = 0

    async for line in read_file(test):
        if line == '':
            elves.append(elf_ttl)
            elf_ttl = 0
        else:
            elf_ttl += int(line)
    elves.append(elf_ttl)
    return elves

async def part_1(test: bool = False) -> int:
    elves = await get_elf_ttls(test)
    return max(elves)

async def part_2(test: bool = False) -> int:
    elves = await get_elf_ttls(test)
    return sum(sorted(elves, reverse=True)[:3])

