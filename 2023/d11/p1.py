def read_file(test: bool = False):
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def build_map(lines, expansion=2):
    rows_populated = set()
    cols_populated = set()
    coords = []
    for ridx, line in enumerate(lines):
        for cidx, char in enumerate(line):
            if char == '#':
                rows_populated.add(ridx)
                cols_populated.add(cidx)
                coords.append([ridx, cidx])

    empty_rows = sorted(list(set(range(ridx)) - rows_populated), reverse=True)

    for row in empty_rows:
        for coord in coords:
            if coord[0] > row:
                coord[0] += expansion - 1

    empty_cols = sorted(list(set(range(cidx)) - cols_populated), reverse=True)
    for col in empty_cols:
        for coord in coords:
            if coord[1] > col:
                coord[1] += expansion - 1

    return coords


def part_1(test=False):
    coords = build_map(read_file(test=test))
    output = 0
    for idx, p1 in enumerate(coords):
        for p2 in coords[idx + 1:]:
            dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
            output += dist

    return output


def part_2(test=False):
    coords = build_map(read_file(test=test), expansion=(100 if test else 1_000_000))
    output = 0
    for idx, p1 in enumerate(coords):
        for p2 in coords[idx + 1:]:
            output += abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

    return output
