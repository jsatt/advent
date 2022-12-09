from typing import Generator


def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def render_map(head_pos, tail_pos):
    cols = max(head_pos[0], tail_pos[0]) + 1
    rows = max(head_pos[1], tail_pos[1]) + 1
    for ridx in range(rows):
        for cidx in range(cols):
            pos = [cidx, rows - ridx - 1]
            if head_pos == pos:
                print('H', end='')
            elif tail_pos == pos:
                print('T', end='')
            else:
                print('.', end='')
        print('\n')

    print('\n')


def find_tail_pos(head, tail, dir):
    xdiff = abs(head[0] - tail[0])
    ydiff = abs(head[1] - tail[1])
    pos = None
    if head == tail or (xdiff <= 1 and ydiff <= 1):
        pos = tail
    else:
        match dir:
            case 'R':
                pos = [head[0] - 1, head[1]]
            case 'L':
                pos = [head[0] + 1, head[1]]
            case 'U':
                pos = [head[0], head[1] - 1]
            case 'D':
                pos = [head[0], head[1] + 1]
    return pos


def part_1(test: bool = False) -> int:
    head_pos = [0, 0]
    tail_pos = [0, 0]
    visited = set([(0,0)])
    for line in read_file(test):
        dir, dist = line.split(' ')
        dist = int(dist)
        for _ in range(dist):
            match dir:
                case 'R':
                    head_pos[0] += 1
                case 'L':
                    head_pos[0] -= 1
                case 'U':
                    head_pos[1] += 1
                case 'D':
                    head_pos[1] -= 1
            tail_pos = find_tail_pos(head_pos, tail_pos, dir)
            visited.add(tuple(tail_pos))

    return len(visited)
