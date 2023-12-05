from typing import AsyncGenerator

import aiofiles


async def read_file(test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()


async def part_1(test=False):
    score = 0
    async for card in read_file(test=test):
        winning, chosen = card.split(': ')[1].split(' | ')
        winning = set(int(x) for x in winning.split(' ') if x)
        chosen = set(int(x) for x in chosen.split(' ') if x)
        matches = len(winning.intersection(chosen))
        if matches:
            score += pow(2, matches - 1)
    return score


async def part_2(test=False):
    cards = {}
    copies = {}
    async for card in read_file(test=test):
        title, numbers = card.split(': ')
        idx = int(title.split()[-1])
        winning, chosen = numbers.split(' | ')
        winning = set(int(x) for x in winning.split(' ') if x)
        chosen = set(int(x) for x in chosen.split(' ') if x)
        match_count = len(winning.intersection(chosen))
        cards[idx] = match_count
        copies[idx] = 1

    for cidx, matches in cards.items():
        for idx in range(copies[cidx]):
            for midx in range(1, matches + 1):
                copies[cidx + midx] += 1

    return sum(copies.values())
