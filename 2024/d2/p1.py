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


def is_safe(levels: list[int]) -> bool:
    prev: int | None = None
    inc: bool | None = None
    for val in levels:
        val = int(val)
        if prev is not None:
            diff = val - prev
            if inc is None:
                inc = diff > 0

            if inc is not (diff > 0):
                return False

            if not (0 < abs(diff) <= 3):
                return False

        prev = val
    return True


async def part_1(test: bool = False) -> int:
    safe_count = 0
    async for line in read_file(test):
        if is_safe(list(map(int, line.split()))):
            safe_count += 1
    return safe_count


async def part_2(test: bool = False) -> int:
    safe_count = 0
    async for line in read_file(test):
        levels = list(map(int, line.split()))
        if is_safe(levels):
            safe_count += 1
        else:
            for i in range(len(levels)):
                new_levels = levels[:i] + levels[i + 1:]
                if is_safe(new_levels):
                    safe_count += 1
                    break
    return safe_count
