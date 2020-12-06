from math import ceil

def read_input(test=False):
    if test:
        filename = 'test_input.txt'
    else:
        filename = 'input.txt'

    with open(filename) as f:
        return [l.strip() for l in f.readlines()]


def div(cur1, cur2, front):
    half = cur1 + ((cur2 - cur1) // 2)
    if front:
        return cur1, half
    return half + 1, cur2

def walk(inst, minv, maxv):
    for i in inst:
        front = i in 'FL'
        minv, maxv = div(minv, maxv, front)
    return minv + round((maxv - minv) / 2)


def read_pass(seat):
    row = walk(seat[:7], 0, 127)
    col = walk(seat[7:], 0, 7)
    return (row * 8) + col


def p1(test=False):
    passes = read_input(test=test)
    seat_ids = [read_pass(s) for s in passes]
    return max(seat_ids)


def p2():
    passes = read_input()
    seat_ids = [read_pass(s) for s in passes]
    empty = set(range(max(seat_ids))) - set(seat_ids)
    for seat_id in empty:
        if seat_id not in seat_ids and seat_id + 1 in seat_ids and seat_id - 1 in seat_ids:
            return seat_id

