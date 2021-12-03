from typing import Generator, List, Sequence
import aiofiles


async def read_file(test: bool = False) -> List[str]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        return [l.strip() for l in await f.readlines()]


async def calculate_life_support(test: bool = False) -> Sequence[str]:
    o2_lines = await read_file(test=test)
    co2_lines = o2_lines.copy()

    for pos in range(len(o2_lines[0])):
        if len(o2_lines) > 1:
            o2_count = 0
            for line in o2_lines:
                if line[pos] == '1':
                    o2_count += 1
            if o2_count >= (len(o2_lines) / 2):
                o2_common = '1'
            else:
                o2_common = '0'
            o2_lines = [l for l in o2_lines if l[pos] == o2_common]

    for pos in range(len(co2_lines[0])):
        if len(co2_lines) > 1:
            co2_count = 0
            for line in co2_lines:
                if line[pos] == '1':
                    co2_count += 1
            if co2_count >= (len(co2_lines) / 2):
                co2_common = '0'
            else:
                co2_common = '1'
            co2_lines = [l for l in co2_lines if l[pos] == co2_common]

    return o2_lines[0], co2_lines[0]


async def part_2(test: bool = False) -> int:
    o2, co2 = await calculate_life_support(test=test)
    return int(o2, 2) * int(co2, 2)
