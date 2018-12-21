import os

## sample
INPUT_FILE = 'test_input.txt'
CYCLES = 10
ANSWER = 1147


## Part 1
INPUT_FILE = 'input.txt'
CYCLES = 10
ANSWER = 598416


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    grid = parse_map(lines)
    render_map(grid)
    for cycle in range(CYCLES):
        grid = tick(grid)
        render_map(grid)

    return score_grid(grid)



def score_grid(grid):
    return len([c for c in grid.values() if c == '|']) * len([c for c in grid.values() if c == '#'])


def parse_map(lines):
    return {
        (xidx, yidx): char
        for yidx, line in enumerate(lines)
        for xidx, char in enumerate(line)
    }


def tick(grid):
    new_grid = grid.copy()
    for coord, content in grid.items():
        adjacents = calc_ajacents(grid, coord)
        if content == '.':
            if len([a for a in adjacents if a == '|']) >= 3:
                new_grid[coord] = '|'
        elif content == '|':
            if len([a for a in adjacents if a == '#']) >= 3:
                new_grid[coord] = '#'
        elif content == '#':
            if not (len([a for a in adjacents if a == '#']) >= 1 and
                len([a for a in adjacents if a == '|']) >= 1 ):
                    new_grid[coord] = '.'

    return new_grid


def calc_ajacents(grid, coord):
    return [
        a for a in (
            grid.get((coord[0] - 1, coord[1] - 1)),
            grid.get((coord[0], coord[1] - 1)),
            grid.get((coord[0] + 1, coord[1] - 1)),
            grid.get((coord[0] - 1, coord[1])),
            grid.get((coord[0] + 1, coord[1])),
            grid.get((coord[0] - 1, coord[1] + 1)),
            grid.get((coord[0], coord[1] + 1)),
            grid.get((coord[0] + 1, coord[1] + 1)),
        )
        if a
    ]


def render_map(grid):
    print('')
    print('')
    print('')
    xs = [c[0] for c in grid.keys()]
    ys = [c[1] for c in grid.keys()]
    for yidx in range(min(ys), max(ys) + 1):
        for xidx in range(min(xs), max(xs) + 1):
            print(grid[xidx, yidx], end='')  # noqa
        print('')
