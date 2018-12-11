import os


def test_locate():
    return run_locate() == 37093


def run_locate():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    points = parse_points(lines)
    mapped = build_map(points)
    area = 0
    for row in mapped:
        for col in row:
            if col < 10000:  # 32 for test_input, 10000 for input
                area += 1
    return area


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
            dist_sum = 0
            for pidx, point in points.items():
                dist_sum += abs(point['x'] - (xidx + minx)) + abs(point['y'] - (yidx + miny))
            mapped[yidx][xidx] = dist_sum
            xidx += 1
        yidx += 1
    return mapped
