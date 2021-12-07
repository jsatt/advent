from typing import Generator, Tuple
import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for l in await f.readlines():
            yield l


def new_board():
    return {'rows': [0] * 5, 'cols': [0] * 5, 'nums': [], 'won': False, 'unmarked': 0}


async def parse_input(test: bool = False):
    _input = read_file(test=test)
    calls = (await _input.__anext__()).strip().split(',')
    boards = []
    async for row in _input:
        row = row.strip()
        if not row:
            board = new_board()
            boards.append(board)
        else:
            board['nums'].append(row.split())
    return calls, boards


async def play_bingo(win: bool = True, test: bool = False) -> Tuple[str, int]:
    calls, boards = await parse_input(test=test)
    for num in calls:
        for board in boards:
            if not board['won']:
                for ridx, row in enumerate(board['nums']):
                    if num in row:
                        cidx = row.index(num)
                        row[cidx] = ''
                        board['cols'][cidx] += 1
                        board['rows'][ridx] += 1
                        if 5 in board['cols'] or 5 in board['rows']:
                            board['unmarked'] = sum([int(c)
                                            for r in board['nums']
                                            for c in r if c])
                            board['won'] = True
            if (win and board['won']) or all([b['won'] for b in boards]):
                return num, board['unmarked']
    return '0', 0


async def part_1(test: bool = False):
    num, unmarked = await play_bingo(test=test)
    return int(num) * unmarked


async def part_2(test: bool = False):
    num, unmarked = await play_bingo(win=False, test=test)
    return int(num) * unmarked
