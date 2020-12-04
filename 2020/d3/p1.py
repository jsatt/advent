
def read_map(test=False):
    if test:
        filename = 'test_input.txt'
    else:
        filename = 'input.txt'

    with open(filename) as f:
        return [l.strip() for l in f.readlines()]


def check_slope(mapping, slope):
    map_height = len(mapping)
    map_width = len(mapping[0])
    cur = (0, 0)
    trees = 0

    while cur[1] < map_height:
        if mapping[cur[1]][cur[0]] == '#':
            trees += 1

        cur = (
            cur[0] + slope[0],
            cur[1] + slope[1]
        )

        if cur[0] >= map_width:
            cur = (cur[0] - map_width, cur[1])
    return trees


def p1(test=False):
    mapping = read_map(test=test)
    slope = (3, 1)
    return check_slope(mapping, slope)


def p2(test=False):
    mapping = read_map(test=test)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    prod = 1

    for slope in slopes:
        mapping = read_map(test=test)
        prod *= check_slope(mapping, slope)

    return prod
