import os


def test_react():
    return run_react() == 6336


def run_react():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        reacted = calc_all(f.read().strip())
    return reacted[0][1]


def react(units):
    idx = 0
    current_units = units

    while idx < len(current_units) - 1:
        unit1 = current_units[idx]
        unit2 = current_units[idx + 1]
        if unit1 != unit2 and unit1.upper() == unit2.upper():
            current_units = current_units[:idx] + current_units[idx + 2:]
            if idx > 0:
                idx -= 1
        else:
            idx += 1

    return current_units


def calc_all(units):
    counts = {}
    for unit in 'abcdefghijklmnopqrstuvwxyz':
        reaction = react(units.replace(unit, '').replace(unit.upper(), ''))
        counts[unit] = len(reaction)
    return sorted(counts.items(), key=lambda x: x[1])
