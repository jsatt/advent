import os


def test_locate():
    return run_locate() == 5358


def run_locate():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    points = parse_points(lines)
    mapped = build_map(points)
    areas = get_counts(mapped)

    return sorted(filter(lambda x: x[1] != 'inf', areas.items()), key=lambda x: x[1], reverse=True)[0][1]


def parse_points(inputs):
    points = {}
    for idx, coord in enumerate(inputs):
        x, y = coord.split(', ')
        points[idx] = {'x': int(x), 'y': int(y)}
    return points


def build_map(points):
    xs = [p['x'] for p in points.values()]
    ys = [p['y'] for p in points.values()]
    minx = min(xs)
    maxx = max(xs)
    miny = min(ys)
    maxy = max(ys)

    mapped = [' '] * (maxy - miny + 1)

    yidx = 0
    while yidx < len(mapped):
        xidx = 0
        mapped[yidx] = [' '] * (maxx - minx + 1)
        while xidx < len(mapped[0]):
            min_dist = None
            closest = ''
            for pidx, point in points.items():
                dist = abs(point['x'] - (xidx + minx)) + abs(point['y'] - (yidx + miny))
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    closest = pidx
                elif dist == min_dist:
                    closest = '.'
            mapped[yidx][xidx] = closest
            xidx += 1
        yidx += 1
    return mapped


def get_counts(mapped):
    areas = {}
    for row_idx, row in enumerate(mapped):
        for col_idx, col in enumerate(row):
            if col not in areas:
                areas[col] = 0

            if col_idx == 0 or row_idx == 0 or col_idx == len(row) - 1 or row_idx == len(mapped) - 1:
                areas[col] = 'inf'
            elif areas[col] != 'inf':
                areas[col] += 1
    return areas
