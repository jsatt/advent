from math import inf
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

async def build_map(test: bool = False) -> Sequence[Sequence[int]]:
    cavemap = [
        [int(c) for c in line.strip()]
        async for line in read_file(test=test)
    ]
    return cavemap


class CaveMap:
    def __init__(self, cavemap: Sequence[Sequence[int]]):
        self.cavemap = cavemap
        self.dimensions = (len(self.cavemap[0]), len(self.cavemap))
        self.visits = []
        self.weights = []
        self.start = (0, 0)

    def get_neighbors(self, pos: Tuple[int, int]) -> Sequence[Tuple[int, int]]:
        nps = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] -1),
            (pos[0], pos[1] + 1),
        ]
        return [
            p for p in nps
            if 0 <= p[0] < self.dimensions[0] and 0 <= p[1] < self.dimensions[1]
        ]

    def is_visited(self, pos):
        return self.visits[pos[0]][pos[1]]

    def find_lowest(self) -> Tuple[int, int]:
        min_weight = inf
        for yidx in range(self.dimensions[1]):
            for xidx in range(self.dimensions[0]):
                if self.weights[xidx][yidx] < min_weight and not self.is_visited((xidx, yidx)):
                    min_weight = self.weights[xidx][yidx]
                    min_pos = (xidx, yidx)
        return min_pos

    def calculate_path(self):
        self.weights = [
            [inf for _ in range(self.dimensions[0])]
            for _ in range(self.dimensions[1])
        ]
        self.weights[self.start[0]][self.start[1]] = 0
        self.visits = [
            [False for _ in range(self.dimensions[0])]
            for _ in range(self.dimensions[1])
        ]
        for _ in range(self.dimensions[1]):
            for _ in range(self.dimensions[0]):
                min_neighbor = self.find_lowest()
                self.visits[min_neighbor[0]][min_neighbor[1]] = True
                neighbors = self.get_neighbors(min_neighbor)
                for neighbor in neighbors:
                    cur_weight = self.weights[neighbor[0]][neighbor[1]]
                    if not self.is_visited(neighbor) and cur_weight > (self.weights[min_neighbor[0]][min_neighbor[1]] + self.cavemap[neighbor[0]][neighbor[1]]):
                        self.weights[neighbor[0]][neighbor[1]] = self.weights[min_neighbor[0]][min_neighbor[1]] + self.cavemap[neighbor[0]][neighbor[1]]


async def part_1(test: bool = False) -> int:
    # breakpoint()
    start_map = await build_map(test=test)
    cavemap = CaveMap(start_map)
    cavemap.calculate_path()
    # breakpoint()
    return cavemap.weights[cavemap.dimensions[0] - 1][cavemap.dimensions[1] - 1]
