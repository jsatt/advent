from functools import reduce
from typing import Generator, Sequence, Tuple

import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l

BRACE_MATCHES = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>',
}

def walk_braces(braces: Sequence) -> Tuple[bool, Sequence[str]]:
    brace_queue = []
    for brace in braces:
        if brace in '([{<':
            brace_queue.append(brace)
        elif brace_queue[-1] in '({[<' and brace == BRACE_MATCHES[brace_queue[-1]]:
            brace_queue.pop()
        else:
            brace_queue.append(brace)
            return False, brace_queue
    return True, brace_queue


def infer_close(braces: Sequence) -> Sequence[str]:
    _, brace_queue = walk_braces(braces)
    closing = [BRACE_MATCHES[p[-1]] for p in reversed(brace_queue)]
    return closing


async def parse_code(test: bool = False) -> Tuple[Sequence, Sequence]:
    errors = []
    good = []
    async for line in read_file(test=test):
        success, braces = walk_braces(line.strip())
        if success:
            good.append(braces)
        else:
            errors.append(braces)
    return good, errors


async def part_1(test: bool = False) -> int:
    score_map = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    return sum([
        score_map[b[-1]]
        for b in (await parse_code(test=test))[1]
    ])


async def part_2(test: bool = False) -> int:
    score_map = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    scores = [
        reduce(lambda x, y: (x * 5) + score_map[y], [0] + infer_close(g))
        for g in (await parse_code(test=test))[0]
    ]

    return sorted(scores)[int(len(scores) / 2)]
