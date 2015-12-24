def calc_floor(directions):
    floor = 0
    for i in directions:
        if i == '(':
            floor += 1
        elif i == ')':
            floor -= 1

    return floor
