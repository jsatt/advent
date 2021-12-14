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


async def parse_instruct(test: bool = False) -> Tuple[Counter, Dict[str, str]]:
    _input = read_file(test=test)
    rules = {}
    template = (await _input.__anext__()).strip()
    polymer = Counter([f'{template[idx]}{template[idx + 1]}' for idx in range(len(template) - 1)])
    polymer[template[-1]] = 1
    await _input.__anext__()

    async for rule in _input:
        pair, elem = rule.strip().split(' -> ')
        rules[pair] = elem
    return polymer, rules


def process_polymer(polymer: Counter, rules: Dict[str, str], steps: int) -> Counter:
    for _ in range(steps):
        new_polymer = Counter()
        for pair, count in polymer.items():
            if pair in rules:
                new_elem = rules[pair]
                elem1, elem2 = pair
                new_polymer[f'{elem1}{new_elem}'] += count
                new_polymer[f'{new_elem}{elem2}'] += count
            else:
                new_polymer[pair] += count
        polymer = new_polymer
    return polymer


def count_elems(polymer: Counter) -> List[Tuple[str, int]]:
    counts = Counter()
    for pair, count in polymer.items():
        counts[pair[0]] += count
    return counts.most_common()


async def part_1(test: bool = False) -> int:
    polymer, rules = await parse_instruct(test=test)
    polymer = process_polymer(polymer, rules, 10)
    counts = count_elems(polymer)
    return counts[0][1] - counts[-1][1]


async def part_2(test: bool = False) -> int:
    polymer, rules = await parse_instruct(test=test)
    polymer = process_polymer(polymer, rules, 40)
    counts = count_elems(polymer)
    return counts[0][1] - counts[-1][1]
