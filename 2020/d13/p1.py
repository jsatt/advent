from math import prod

FILENAME = 'test_input.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return f.readlines()


def p1():
    time, buses = read_input()
    time = int(time)
    buses = [int(b) for b in buses.split(',') if b != 'x']
    ticks = 0
    while True:
        cur_time = time + ticks
        for bus in buses:
            if cur_time % bus == 0:
                return bus * ticks
        ticks += 1


def calc_ctr(bus, rem, buses):
    ni = prod([x[0] for x in buses if x[0] != bus])
    x = 0
    for x in range(bus):
        if (x * ni) % bus == 1:
            break
    return (-rem % bus) * ni * x


def p2():
    _, buses = read_input()
    buses = [(int(b),  i) for i, b in enumerate(buses.split(',')) if b != 'x']
    return sum([calc_ctr(b[0], b[1], buses) for b in buses]) % prod([b[0] for b in buses])
