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


def get_coords(
        start: tuple[int, int],
        grid_size: int,
        match_size: int = 4) -> list[list[tuple[int, int]]]:
    coords: list[list[tuple[int, int]]] = []
    steps = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    )
    for x_step, y_step in steps:
        dir_coords: list[tuple[int, int]] = [start]
        curr_step: tuple[int, int] = start
        while (0 <= curr_step[1] + y_step < grid_size
                and 0 <= curr_step[0] + x_step < grid_size
                and len(dir_coords) < match_size):
            curr_step = (curr_step[0] + x_step, curr_step[1] + y_step)
            dir_coords.append(curr_step)
        if len(dir_coords) == match_size:
            coords.append(dir_coords)
        # print(x_step, y_step, curr_step)
        # print(coords)

    return coords


async def part_1(test: bool = False) -> int:
    grid = [list(line) async for line in read_file(test=test)]
    grid_size = len(grid)
    count = 0
    for x in range(grid_size):
        for y in range(grid_size):
            for coord in get_coords((x, y), grid_size, 4):
                chars = ''.join([grid[yc][xc] for xc, yc in coord])
                if chars == 'XMAS':
                    count += 1

    return count
