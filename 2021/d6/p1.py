from typing import Dict

import aiofiles


async def read_file(test: bool = False) -> str:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        return await f.read()


async def spawn_fish(days=18, test: bool = False) -> Dict[int, int]:
    fishes = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for fish in (await read_file(test=test)).split(','):
        fishes[int(fish)] += 1

    prime = {}
    pointers = list(range(7))
    for _ in range(days):
        pointer = pointers[0]
        count = fishes[pointer]
        fishes[pointer] += prime.pop(pointer, 0)
        num_prime = pointer + 2
        if num_prime > 6:
            num_prime -= 7
        prime[num_prime] = count
        pointers.append(pointers.pop(0))

    for pointer, count in prime.items():
        fishes[pointer] += count
    return fishes


async def part_1(days: int = 80, test: bool = False) -> int:
    fishes = await spawn_fish(days, test=test)
    return sum(fishes.values())


async def part_2(days: int = 256, test: bool = False) -> int:
    fishes = await spawn_fish(days, test=test)
    return sum(fishes.values())
