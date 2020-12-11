FILENAME = 'test_input.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return [list(l.strip()) for l in f.readlines()]


def get_seat(row, seat, seats):
    if 0 <= row < len(seats) and 0 <= seat < len(seats[0]):
        return seats[row][seat]


def check_surrounding(row, seat, seats):
    surrounding = [
        x for x in (
            get_seat(row - 1, seat - 1, seats),
            get_seat(row - 1, seat, seats),
            get_seat(row - 1, seat + 1, seats),
            get_seat(row, seat - 1, seats),
            get_seat(row, seat + 1, seats),
            get_seat(row + 1, seat - 1, seats),
            get_seat(row + 1, seat, seats),
            get_seat(row + 1, seat + 1, seats),
        )
        if x == '#'
    ]
    return len(surrounding)



def cycle_seats(seats):
    change = False
    new_seats = [r.copy() for r in seats]
    for ridx, row in enumerate(seats):
        for sidx, seat in enumerate(row):
            occupied = check_surrounding(ridx, sidx, seats)
            if seat == 'L' and occupied == 0:
                new_seats[ridx][sidx] = '#'
                change = True
            elif seat == '#' and occupied >= 4:
                new_seats[ridx][sidx] = 'L'
                change = True

    return change, new_seats


def count_seats(seats):
    return sum([
        len([s for s in row if s == '#'])
        for row in seats
    ])

def render_seats(seats):
    for row in seats:
        print(''.join(row))
    print('----------------')

def p1():
    seats = read_input()
    change = True
    while change:
        # render_seats(seats)
        change, seats = cycle_seats(seats)

    return count_seats(seats)
