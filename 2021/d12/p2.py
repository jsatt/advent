from collections import deque, Counter
from typing import Dict, Generator, List

import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.is_big = name.isupper()
        self.connected = []

    def __repr__(self):
        return f'<Cave: {self.name}, {[n.name for n in self.connected]}>'

    def __eq__(self, other):
        return self.name == other.name


async def build_map(test: bool = False) -> Dict[str, Cave]:
    cavemap = {}
    async for line in read_file(test=test):
        c1, c2 = line.strip().split('-')
        if c1 not in cavemap:
            cavemap[c1] = Cave(c1)
        if c2 not in cavemap:
            cavemap[c2] = Cave(c2)
        cavemap[c1].connected.append(cavemap[c2])
        cavemap[c2].connected.append(cavemap[c1])
    return cavemap


def walk(start: Cave, until: Cave, allow_dupe_small: bool = False) -> List[List[Cave]]:
    paths = deque([[start]])
    valid = []
    while paths:
        path = paths.pop()
        current_node = path[-1]

        if current_node == until:
            valid.append(path)
            continue

        for node in current_node.connected:
            if allow_dupe_small:
                small_dupes = 2 in Counter([node.name for node in path if not node.is_big]).values()
            else:
                small_dupes = True
            if node != start and (node.is_big or not small_dupes or (small_dupes and node not in path)):
                paths.append(path + [node])

    return valid


async def part_1(test: bool = False) -> int:
    map = await build_map(test=test)
    paths = walk(map['start'], map['end'])
    return len(paths)


async def part_2(test: bool = False) -> int:
    map = await build_map(test=test)
    paths = walk(map['start'], map['end'], allow_dupe_small=True)
    return len(paths)
