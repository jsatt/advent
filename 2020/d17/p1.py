from collections import defaultdict

FILENAME = 'test_input.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return parse_board(f.readlines())

def get_fresh_board():
    return defaultdict(lambda: defaultdict(lambda: defaultdict(bool)))


def parse_board(lines):
    board = get_fresh_board()
    extents = [[0, 0], [0, len(lines) - 1], [0, len(lines[0].strip()) - 1]]
    for x, xval in enumerate(lines):
        for y, yval in enumerate(xval.strip()):
            board[0][x][y] = yval == '#'
    return board, extents


def check_neighbors(x, y, z, board):
    return len([
        True
        for zi in range(z - 1, z + 2)
        for xi in range(x- 1, x + 2)
        for yi in range(y - 1,  y + 2)
        if not (z, x, y) == (zi, xi, yi) and board[zi][xi][yi]
    ])


def play_cycle(board, extents):
    new_board = get_fresh_board()
    new_extents = [(i[0] - 1, i[1] + 1) for i in extents]
    for z in range(new_extents[0][0], new_extents[0][1] + 1):
        for x in range(new_extents[1][0], new_extents[1][1] + 1):
            for y in range(new_extents[2][0], new_extents[2][1] + 1):
                val = board[z][x][y]
                neighbor_count= check_neighbors(x, y, z, board)
                if val:
                    new_board[z][x][y] = neighbor_count in [2, 3]
                elif not val:
                    new_board[z][x][y] = neighbor_count == 3
    return new_board, new_extents


def count_cubes(board):
    return len([
        z
        for x in board.values()
        for y in x.values()
        for z in y.values()
        if z
    ])


def render_board(board):
    for zi, z in board.items():
        print(zi)
        for x in z.values():
            print(''.join(['#' if y else '.' for y in x.values()]))
    print('=====')


def p1():
    board, extents = read_input()
    # print(extents)
    # render_board(board)
    for _ in range(6):
        board, extents = play_cycle(board, extents)
        # print(extents)
        # render_board(board)

    return count_cubes(board)
