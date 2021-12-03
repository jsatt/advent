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


async def calculate_power_rates(test: bool = False) -> Sequence[str]:
    counts = []
    lines = 0
    gamma = ''
    epsilon = ''

    async for line in read_file(test=test):
        lines += 1
        value = line.strip()

        if not counts:
            counts = [0] * len(value)

        for idx, bit in enumerate(value):
            if bit == '1':
                counts[idx] += 1

    threshold = lines / 2
    for count in counts:
        if count > threshold:
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    return gamma, epsilon


async def part_1(test: bool = False) -> int:
    gamma, epsilon = await calculate_power_rates(test=test)
    return int(gamma, 2) * int(epsilon, 2)
