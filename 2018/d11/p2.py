GRID_SIZE = 300

# Sample 1
# GRID_SERIAL = 18
# ANSWER_POWER = 113
# ANSWER_COORDS = 90, 269
# ANSWER_SIZE = 16
## sample 2
# GRID_SERIAL = 42
# ANSWER_POWER = 119
# ANSWER_COORDS = 232, 251
# ANSWER_SIZE = 12

## Input
GRID_SERIAL = 7511
ANSWER_POWER = 147
ANSWER_COORDS = 235, 288
ANSWER_SIZE = 13


def test_day():
    return run_day() == (ANSWER_POWER, ANSWER_COORDS, ANSWER_SIZE)


def run_day():
    cell_cache = {}
    absolute_max_level = 0
    absolute_max_coords = None
    absolute_max_size = 0
    for window in range(1, GRID_SIZE + 1):
        print('calculating: {}'.format(window))
        max_level, max_coords = walk_cells(GRID_SIZE, window, GRID_SERIAL, cell_cache)
        if max_level > absolute_max_level:
            absolute_max_level = max_level
            absolute_max_coords = max_coords
            absolute_max_size = window
    return absolute_max_level, absolute_max_coords, absolute_max_size


def calc_cell(x, y, serial, cache):
    level = cache.get((x, y, 1))
    if level is None:
        rack_id = x + 10
        start_level = rack_id * y
        factor = ((start_level + serial) * rack_id) % 1000 // 100
        level = factor - 5
        cache[x, y, 1] = level
    return level


def walk_cells(size, window_size, serial, cache):
    max_level = 0
    max_coords = None
    # import pdb; pdb.set_trace()  # XXX BREAKPOINT
    for yidx in range(1, size - window_size + 2):
        for xidx in range(1, size - window_size + 2):
            total = cache.get((xidx, yidx, window_size - 1), 0)
            for offset in range(window_size):
                total += calc_cell(xidx + window_size - 1, yidx + offset, serial, cache)
                if offset < window_size - 1:
                    total += calc_cell(xidx + offset, yidx + window_size - 1, serial, cache)

            cache[xidx, yidx, window_size] = total
            if total > max_level:
                max_level = total
                max_coords = (xidx, yidx)
    return max_level, max_coords
