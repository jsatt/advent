import os


def test_check_ids():
    return run_check() == 3952


def run_check():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        return check_ids(
            [
                x
                for x in f.read().splitlines()
                if x
            ]
        )


def check_ids(ids):
    dups = 0
    trips = 0
    for item in ids:
        counts = {}
        for letter in item:
            if letter not in counts:
                counts[letter] = 0
            counts[letter] += 1
        if 2 in counts.values():
            dups += 1
        if 3 in counts.values():
            trips += 1
    return dups * trips
