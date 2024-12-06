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


async def part_2(test: bool = False) -> int:
    grid = [list(line) async for line in read_file(test=test)]
    grid_size = len(grid)
    count = 0
    for x in range(grid_size):
        for y in range(grid_size):
            pos = (x, y)
            if (grid[y][x] == 'A'
                    and 0 < pos[0] < grid_size - 1
                    and 0 < pos[0] < grid_size + 1
                    and 0 < pos[1] < grid_size - 1
                    and 0 < pos[1] < grid_size + 1
                    and ''.join([
                        grid[pos[1] - 1][pos[0] - 1],
                        grid[pos[1]][pos[0]],
                        grid[pos[1] + 1][pos[0] + 1]
                    ]) in ['MAS', 'SAM']
                    and ''.join([
                        grid[pos[1] - 1][pos[0] + 1],
                        grid[pos[1]][pos[0]],
                        grid[pos[1] + 1][pos[0] - 1]
                    ]) in ['MAS', 'SAM']):
                count += 1

    return count
