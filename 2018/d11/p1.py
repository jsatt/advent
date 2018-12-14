GRID_SIZE = 300

# Sample 1
# GRID_SERIAL = 18
# ANSWER_POWER = 29
# ANSWER_COORDS = 33, 45
## sample 2
# GRID_SERIAL = 42
# ANSWER_POWER = 30
# ANSWER_COORDS = 21, 61

## Input
GRID_SERIAL = 7511
ANSWER_POWER = 34
ANSWER_COORDS = 21, 22


def test_day():
    return run_day() == (ANSWER_POWER, ANSWER_COORDS)


def run_day():
    max_level, max_coords = walk_cells(GRID_SIZE, GRID_SERIAL)
    return max_level, max_coords


def calc_cell(x, y, serial, cache):
    if (x, y) not in cache:
        rack_id = x + 10
        start_level = rack_id * y
        factor = ((start_level + serial) * rack_id) % 1000 // 100
        level = factor - 5
        cache[x,y] = level
    return cache[x, y]


def walk_cells(size, serial):
    max_level = 0
    max_coords = None
    level_cache = {}
    for yidx in range(size - 3):
        for xidx in range(size - 3):
            total = (
                calc_cell(xidx, yidx, serial, level_cache) + calc_cell(xidx + 1, yidx, serial, level_cache) + calc_cell(xidx + 2, yidx, serial, level_cache) +
                calc_cell(xidx, yidx + 1, serial, level_cache) + calc_cell(xidx + 1, yidx + 1, serial, level_cache) + calc_cell(xidx + 2, yidx + 1, serial, level_cache) +
                calc_cell(xidx, yidx + 2, serial, level_cache) + calc_cell(xidx + 1, yidx + 2, serial, level_cache) + calc_cell(xidx + 2, yidx + 2, serial, level_cache)
            )
            if total > max_level:
                max_level = total
                max_coords = (xidx, yidx)
    return max_level, max_coords
