import re

import aiofiles


async def read_file(test: bool = False) -> str:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        return await f.read()


async def part_1(test: bool = False) -> int:
    pairs = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', await read_file(test=test))
    return sum(map(lambda x: int(x[0]) * int(x[1]), pairs))


async def part_2(test: bool = False) -> int:
    instructions = re.findall(
        r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))',
        await read_file(test=test))
    enabled = True
    out = 0
    for x, y, do_i, dont_i in instructions:
        if do_i:
            enabled = True
        elif dont_i:
            enabled = False
        else:
            if enabled:
                out += int(x) * int(y)

    return out
