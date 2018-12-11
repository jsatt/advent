import os


def test_check_ids():
    return run_check() == 'vtnikorkulbfejvyznqgdxpaw'


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
    hashes = {}

    for item in ids:
        for idx in range(len(item)):
            moded = '{}_{}'.format(item[:idx], item[idx + 1:])
            if moded not in hashes:
                hashes[moded] = 0
            hashes[moded] += 1

    for k, v in hashes.items():
        if v > 1:
            return k.replace('_', '')
