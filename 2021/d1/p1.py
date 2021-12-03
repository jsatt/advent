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


async def count_increases_window(window_size: int = 1, test: bool = False) -> int:
    inc_count = 0
    readings = []
    current_point = window_size
    prev_point = window_size + 1

    async for line in read_file(test=test):
        readings.append(int(line))
        if (
            len(readings) >= prev_point and
            sum(readings[-current_point:]) > sum(readings[-prev_point:-1])
        ):
            inc_count += 1
    return inc_count


async def part_1(test: bool = False):
    return await count_increases_window(1, test=test)


async def part_2(test: bool = False):
    return await count_increases_window(3, test=test)
