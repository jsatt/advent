from collections import Counter
from typing import Dict, Generator, List, Tuple

import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l


async def parse_instruct(test: bool = False) -> Tuple[List[str], Dict[str, str]]:
    _input = read_file(test=test)
    rules = {}
    template = list((await _input.__anext__()).strip())
    await _input.__anext__()

    async for rule in _input:
        pair, elem = rule.strip().split(' -> ')
        rules[pair] = elem
    return template, rules


def process_polymer(polymer: list, rules: Dict[str, str]) -> list:
    new_polymer = []
    max_idx = len(polymer)
    for idx in range(max_idx - 1):
        elem1, elem2 = polymer[idx:idx + 2]
        new_polymer.append(elem1)
        new_polymer.append(rules[f'{elem1}{elem2}'])
        if idx == max_idx - 2:
            new_polymer.append(elem2)
    return new_polymer


async def part_1(steps = 10, test: bool = False) -> int:
    polymer, rules = await parse_instruct(test=test)
    for _ in range(steps):
        polymer = process_polymer(polymer, rules)
    counts = Counter(polymer).most_common()
    return counts[0][1] - counts[-1][1]
