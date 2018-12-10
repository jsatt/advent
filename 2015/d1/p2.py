def calc_floor(directions):
    floor = 0
    for i, inst in enumerate(directions):
        if inst == '(':
            floor += 1
        elif inst == ')':
            floor -= 1

        if floor < 0:
            return i + 1

    return floor
