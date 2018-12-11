import os.path


def test_adjust_freq():
    return run_adjust_freq() == 500


def run_adjust_freq():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        return adjust_freq(
            (
                int(x)
                for x in f.read().splitlines()
                if x
             )
        )


def adjust_freq(inputs):
    freq = 0
    for change in inputs:
        freq += change
    return freq
