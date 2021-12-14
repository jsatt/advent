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
        self.visited = False

    def reset(self):
        self.visited = False

    def visit(self):
        self.visited = True

    def can_visit(self) -> bool:
        return self.is_big or not self.visited

    def __repr__(self) -> str:
        return f'<Cave: {self.name}, {[n.name for n in self.connected]}>'


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


def walk(cave: Cave) -> List[List[Cave]]:
    paths = []
    if cave.name == 'end':
        return [[cave]]
    cave.visit()
    for link in cave.connected:

        if link.can_visit():
            for path in walk(link):
                paths.append([cave] + path)
    cave.reset()

    return paths


async def part_1(test: bool = False) -> int:
    map = await build_map(test=test)
    paths = walk(map['start'])
    return len(paths)
