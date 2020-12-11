FILENAME = 'test_input.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return build_map(f.readlines())


def build_map(lines):
    seat_map: dict = {
        (ridx, cidx): s
        for ridx, r in enumerate(lines)
        for cidx, s in enumerate(r.strip())
        if s in 'L#'
    }
    seat_map['height'] = len(lines)
    seat_map['width'] = len(lines[0].strip())
    return seat_map


def get_seat(row, col, row_dir, col_dir, seats):
    coords = (row, col)
    val = None
    while val is None and 0 <= coords[0] < seats['height'] and 0 <= coords[1] < seats['width']:
        coords = (coords[0] + row_dir, coords[1] + col_dir)
        val = seats.get(coords)
    return val


def check_surrounding(row, col, seats):
    surrounding = [
        x for x in (
            get_seat(row, col, -1,  -1, seats),
            get_seat(row, col, -1,  0, seats),
            get_seat(row, col, -1,  1, seats),
            get_seat(row, col, 0,  -1, seats),
            get_seat(row, col, 0,  1, seats),
            get_seat(row, col, 1,  -1, seats),
            get_seat(row, col, 1,  0, seats),
            get_seat(row, col, 1,  1, seats),
        )
        if x == '#'
    ]
    return len(surrounding)


def cycle_seats(seats):
    new_seats = seats.copy()
    for ridx in range(seats['height']):
        for cidx in range(seats['width']):
            occupied = check_surrounding(ridx, cidx, seats)
            seat = seats.get((ridx, cidx))
            if seat == 'L' and occupied == 0:
                new_seats[ridx, cidx] = '#'
            elif seat == '#' and occupied >= 5:
                new_seats[ridx, cidx] = 'L'
    return new_seats


def count_seats(seats):
    return len([
        s
        for s in seats.values()
        if s == '#'
    ])


def render_seats(seats):
    for row in range(seats['height']):
        row_out = ''
        for col in range(seats['width']):
            row_out += seats.get((row, col), '.')

        print(row_out)
    print('----------------')


def p2():
    seats = read_input()
    while True:
        # render_seats(seats)
        new_seats = cycle_seats(seats)
        if new_seats == seats:
            break
        seats = new_seats

    return count_seats(new_seats)
