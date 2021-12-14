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


async def build_map(test: bool = False) -> Tuple[set, Sequence[Tuple[str, int]]]:
    dotmap = set()
    folds = []
    async for line in read_file(test=test):
        if not line.strip():
            continue
        elif line.startswith('fold along'):
            orientation, pos = line.strip().split(' ')[2].split('=')
            folds.append((orientation, int(pos)))
        else:
            x, y = map(int, line.strip().split(','))
            dotmap.add((x, y))
    return dotmap, folds


def render_map(dotmap: set):
    height = max([y for _, y in dotmap])
    width = max([x for x, _ in dotmap])
    for yidx in range(height + 1):
        for xidx in range(width + 1):
            print('#' if (xidx, yidx) in dotmap else '.', end='')
        print('')


def perform_fold(dotmap: set, orientation: str, pos: int) -> set:
    new_map = set()
    for x, y in dotmap:
        if orientation == 'y' and y > pos:
                y = pos - (y - pos)
        elif orientation == 'x' and x > pos:
            x = pos - (x - pos)
        new_map.add((x, y))
    return new_map


async def part_1(test: bool = False) -> int:
    dotmap, folds = await build_map(test=test)
    dotmap = perform_fold(dotmap, *folds[0])
    return len(dotmap)


async def part_2(test: bool = False):
    dotmap, folds = await build_map(test=test)
    for fold in folds:
        dotmap = perform_fold(dotmap, *fold)
    render_map(dotmap)
