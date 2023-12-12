def read_file(test=None):
    if test:
        file_name = f'test_input_{test}.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def is_valid_connection(shape, target, dir):
    valid = []
    match shape, dir:
        case 'F', 'E':
            valid = ['-', 'J', '7', 'S']
        case 'F', 'S':
            valid = ['|', 'L', 'J', 'S']
        case '7', 'W':
            valid = ['-', 'L', 'F', 'S']
        case '7', 'S':
            valid = ['|', 'L', 'J', 'S']
        case 'J', 'N':
            valid = ['|', '7', 'F', 'S']
        case 'J', 'W':
            valid = ['-', 'F', 'L', 'S']
        case 'L', 'N':
            valid = ['|', 'F', '7', 'S']
        case 'L', 'E':
            valid = ['-', '7', 'J', 'S']
        case '|', 'N':
            valid = ['7', 'F', '|', 'S']
        case '|', 'S':
            valid = ['|', 'J', 'L', 'S']
        case '-', 'E':
            valid = ['-', 'J', '7', 'S']
        case '-', 'W':
            valid = ['-', 'L', 'F', 'S']
        case 'S', 'N':
            valid = ['F', '7', '|']
        case 'S', 'E':
            valid = ['-', 'J', '7']
        case 'S', 'S':
            valid = ['|', 'L', 'J']
        case 'S', 'W':
            valid = ['-', 'F', 'L']
    return target in valid


def parse_map(lines):
    map = {}
    start_idx = None
    rows = len(lines)
    cols = len(lines[0])
    for ridx in range(rows):
        line = lines[ridx]
        for cidx in range(cols):
            shape = line[cidx]
            if shape == 'S':
                start_idx = (ridx, cidx)
                map[start_idx] = {'shape': shape, 'dist': 0, 'targets': []}
            valid_targets = []
            for dir, tidxr, tidxc in [('N', ridx - 1, cidx),
                                      ('E', ridx, cidx + 1),
                                      ('S', ridx + 1, cidx),
                                      ('W', ridx, cidx - 1)]:

                if tidxr < 0 or tidxr >= rows or tidxc < 0 or tidxc >= cols:
                    continue

                target = lines[tidxr][tidxc]
                if is_valid_connection(shape, target, dir):
                    valid_targets.append((tidxr, tidxc))

            if len(valid_targets) == 2:
                map[ridx, cidx] = {'shape': shape, 'targets': valid_targets}
    return map, start_idx


def part_1(test=None):
    map, start_idx = parse_map(list(read_file(test=test)))
    start_targets = map[start_idx]['targets']
    map[start_targets[0]]['targets'].remove(start_idx)
    map[start_targets[1]]['targets'].remove(start_idx)
    idxs = {'L': start_targets[0], 'R': start_targets[1]}
    steps = 0
    while True:
        steps += 1
        if idxs['L'] == idxs['R']:
            output = steps
            break
        for dir in ['L', 'R']:
            target = map[idxs[dir]]
            new_idx = target['targets'][0]
            map[new_idx]['targets'].remove(idxs[dir])
            idxs[dir] = new_idx

    return output
