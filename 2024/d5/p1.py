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
    lines = read_file(test)
    order_rules: dict[str, set[str]] = defaultdict(set)
    async for line in lines:
        if line == '':
            break
        k, v = line.split('|')
        order_rules[v].add(k)

    out = 0
    async for line in lines:
        update = line.split(',')
        if is_valid_order(update, order_rules):
            middle = update[len(update) // 2]
            out += int(middle)
    return out


def is_valid_order(pages: list[str], order_rules: dict[str, set[str]]):
    for idx, page in enumerate(pages):
        if order_rules[page].intersection(set(pages[idx + 1:])):
            return False
    return True


def find_max_order(order_rules: dict[str, set[str]], page: str, cache: dict[str, int]) -> int:
    # print(CACHE_ORDER, page)
    try:
        result: int = cache[page]
    except KeyError:
        if page not in order_rules:
            # print(page, 0)
            result = 0
        else:
            result = 1 + max(find_max_order(order_rules, page, cache) for page in order_rules[page])
            # print(page, 'rec')
        cache[page] = result
    return result


async def part_2(test: bool = False) -> int:
    lines = read_file(test)
    order_rules: dict[str, set[str]] = defaultdict(set)
    async for line in lines:
        if line == '':
            break
        k, v = line.split('|')
        order_rules[v].add(k)

    updates = [line.split(',') async for line in lines]

    out = 0
    for update in updates:
        cache: dict[str, int] = {}
        correct_order = {
            p: find_max_order({
                k: v
                for k, v in order_rules.items()
                if k in update
            }, p, cache)
            for p in update
        }
        fixed_update = sorted(update, key=lambda x: correct_order[x])
        if not update == fixed_update:
            middle_idx = round(len(update) // 2)
            middle = fixed_update[middle_idx]
            out += int(middle)

    return out
