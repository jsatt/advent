from typing import AsyncGenerator, Iterable
from collections import deque

import aiofiles

async def read_file(test: bool = False) -> AsyncGenerator[str, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()

POINTS = {
    'A': 1,
    'B': 2,
    'C': 3,
    'X': 1,
    'Y': 2,
    'Z': 3,
}

async def part_1(test: bool = False) -> int:
    score = 0
    async for round in read_file(test):
        p1, p2 = round.split(' ')
        diff = POINTS[p1] - POINTS[p2]
        if diff == 0: # draw
           outcome = 3
        elif diff == 1 or diff == -2: # lose
            outcome = 0
        else: # win
            outcome = 6
        round = POINTS[p2] + outcome
        score += round
    return score


async def part_2(test: bool = False) -> int:
    score = 0
    plays = deque(['A', 'B', 'C'])
    async for round in read_file(test):
        p1, p2 = round.split(' ')
        plays.rotate(1-plays.index(p1))
        if p2 == 'Y': # draw
            outcome = 3
            pscore = POINTS[p1]
        elif p2 == 'X': # lose
            outcome = 0
            pscore = POINTS[plays[0]]
        else: # Z win
            outcome = 6
            pscore = POINTS[plays[2]]
        score += outcome + pscore
    return score

# P R  2 - 1 = 1 L
# S P  3 - 2 = 1 L
# R S  1 - 3 = -2 L
# R P  1 - 2  = -1 W
# P S  2 - 3 = -1 W
# S R  3 - 1 = 2 W
# R R  1 - 1 = 0 D
# P P  2 - 2 = 0 D
# S S  3 - 3 = 0 D
