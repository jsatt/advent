from collections.abc import AsyncGenerator
from itertools import cycle

import aiofiles


async def read_file(test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()


def walk_until_obstacle(curr_pos: tuple[int, int], direction: str, floor_map: list[tuple[int, int]], size: tuple[int, int], visited: set[tuple[int, int]]):
    steps = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0),
    }
    obstructed = False
    end_walk = False
    while not obstructed:
        dir_steps = steps[direction]
        new_pos = (curr_pos[0] + dir_steps[0], curr_pos[1] + dir_steps[1])
        if new_pos in floor_map:
            obstructed = True
        else:
            visited.add(curr_pos)
            curr_pos = new_pos
        if not (0 <= curr_pos[0] < size[0] and 0 <= curr_pos[1] < size[1]):
            end_walk = True
            break
    return curr_pos, end_walk


def on_board(curr_pos: tuple[int, int], size: tuple[int, int]) -> bool:
    return 0 <= curr_pos[0] < size[0] and 0 <= curr_pos[1] < size[1]


async def part_1(test: bool = False) -> int:
    curr_pos: tuple[int, int] | None
    direction = 'N'
    floor_map: list[tuple[int, int]] = []
    y = 0
    async for line in read_file(test):
        x = 0
        for c in line:
            if c == '#':
                floor_map.append((x, y))
            elif c == '^':
                curr_pos = (x, y)
            x += 1
        y += 1
    size = (x, y)

    dirs = cycle(['N', 'E', 'S', 'W'])
    visited: set[tuple[int, int]] = set()
    started = False
    while not started or on_board(curr_pos, size):
        started = True
        new_pos, end_walk = walk_until_obstacle(
            curr_pos,  direction, floor_map, size, visited)
        direction = next(dirs)
        if end_walk:
            break
        curr_pos = new_pos
    return len(visited)
