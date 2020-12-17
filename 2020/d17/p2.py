from collections import defaultdict

FILENAME = 'test_input.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return parse_board(f.readlines())

def get_fresh_board():
    return defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(bool))))


def parse_board(lines):
    board = get_fresh_board()
    extents = [[0, 0], [0, 0], [0, len(lines) - 1], [0, len(lines[0].strip()) - 1]]
    for x, xval in enumerate(lines):
        for y, yval in enumerate(xval.strip()):
            board[0][0][x][y] = yval == '#'
    return board, extents


def check_neighbors(w, x, y, z, board):
    return len([
        True
        for wi in range(w - 1, w + 2)
        for zi in range(z - 1, z + 2)
        for xi in range(x- 1, x + 2)
        for yi in range(y - 1,  y + 2)
        if not (w, z, x, y) == (wi, zi, xi, yi) and board[wi][zi][xi][yi]
    ])


def play_cycle(board, extents):
    new_board = get_fresh_board()
    new_extents = [(i[0] - 1, i[1] + 1) for i in extents]
    for w in range(new_extents[1][0], new_extents[1][1] + 1):
        for z in range(new_extents[0][0], new_extents[0][1] + 1):
            for x in range(new_extents[2][0], new_extents[2][1] + 1):
                for y in range(new_extents[3][0], new_extents[3][1] + 1):
                    val = board[w][z][x][y]
                    neighbor_count = check_neighbors(w, x, y, z, board)
                    if val:
                        new_board[w][z][x][y] = neighbor_count in [2, 3]
                    elif not val:
                        new_board[w][z][x][y] = neighbor_count == 3
    return new_board, new_extents


def count_cubes(board):
    return len([
        y
        for w in board.values()
        for z in w.values()
        for x in z.values()
        for y in x.values()
        if y
    ])


def render_board(board):
    for wi, w in board.items():
        for zi, z in w.items():
            print(zi, wi)
            for x in z.values():
                print(''.join(['#' if y else '.' for y in x.values()]))
    print('=====')


def p2():
    board, extents = read_input()
    # print(extents)
    # render_board(board)
    for _ in range(6):
        board, extents = play_cycle(board, extents)
        # print(extents)
        # render_board(board)

    return count_cubes(board)

