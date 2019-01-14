# sample
CAVE_DEPTH = 510
TARGET = 10, 10
ANSWER = 114

# part 1
CAVE_DEPTH = 10914
TARGET = 9, 739
ANSWER = 7380


def test_day():
    return run_day() == ANSWER


def run_day():
    grid = build_map(CAVE_DEPTH, TARGET)
    render_map(grid, TARGET)
    return calc_risk(grid)


def build_map(depth, target_coord):
    level = {}

    for yidx in range(target_coord[1] + 1):
        for xidx in range(target_coord[0] + 1):
            if (xidx, yidx) == (0, 0) or (xidx, yidx) == target_coord:
                geo_idx = 0
            elif yidx == 0:
                geo_idx = xidx * 16807
            elif xidx == 0:
                geo_idx = yidx * 48271
            else:
                geo_idx = level[xidx - 1, yidx] * level[xidx, yidx - 1]
            level[xidx, yidx] = (geo_idx + depth) % 20183
    return level


def calc_risk(grid):
    max_x = max([r[0] for r in grid.keys()])
    max_y = max([r[1] for r in grid.keys()])
    risk = 0

    for yidx in range(max_y + 1):
        for xidx in range(max_x + 1):
            risk += grid[xidx, yidx] % 3

    return risk


def render_map(grid, target_coord):
    max_x = max([r[0] for r in grid.keys()])
    max_y = max([r[1] for r in grid.keys()])
    types = '.=|'

    for yidx in range(max_y + 1):
        for xidx in range(max_x + 1):
            if (xidx, yidx) == (0, 0):
                print('M', end='')

            elif (xidx, yidx) == target_coord:
                print('T', end='')
            else:
                print(types[grid[xidx, yidx] % 3], end='')
        print('')
