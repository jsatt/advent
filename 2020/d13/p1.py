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
