import numpy

GRID_SIZE = 300

# Sample 1
GRID_SERIAL = 18
ANSWER_POWER = 113
ANSWER_COORDS = 90, 269
ANSWER_SIZE = 16
## sample 2
# GRID_SERIAL = 42
# ANSWER_POWER = 119
# ANSWER_COORDS = 232, 251
# ANSWER_SIZE = 12

## Input
# GRID_SERIAL = 7511
# ANSWER_POWER = 147
# ANSWER_COORDS = 235, 288
# ANSWER_SIZE = 13


def test_day():
    return run_day() == (ANSWER_POWER, ANSWER_COORDS, ANSWER_SIZE)


def run_day():
    absolute_max_level = 0
    absolute_max_coords = None
    absolute_max_size = 0
    cells = calc_cells(GRID_SIZE, GRID_SERIAL)
    for window in range(1, GRID_SIZE + 1):
        print('calculating: {}'.format(window))
        max_level, max_coords = walk_cells(cells, window)
        if max_level > absolute_max_level:
            absolute_max_level = max_level
            absolute_max_coords = max_coords
            absolute_max_size = window
    return absolute_max_level, absolute_max_coords, absolute_max_size


def calc_cells(size, serial):
    cells = []
    for yidx in range(1, size + 1):
        row = []
        cells.append(row)
        for xidx in range(1, size + 1):
            row.append(calc_cell(xidx, yidx, serial))
    return numpy.array(cells)


def calc_cell(x, y, serial):
    rack_id = x + 10
    start_level = rack_id * y
    factor = ((start_level + serial) * rack_id) % 1000 // 100
    level = factor - 5
    return level


def walk_cells(cells, window_size):
    max_level = 0
    max_coords = None
    # import pdb; pdb.set_trace()  # XXX BREAKPOINT
    for yidx in range(1, len(cells) - window_size):
        for xidx in range(1, len(cells) - window_size):
            total = numpy.sum(cells[yidx:yidx + window_size, xidx:xidx + window_size])
            if total > max_level:
                max_level = total
                max_coords = (xidx + 1, yidx + 1)
    return max_level, max_coords
