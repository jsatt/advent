import os.path


def test_adjust_freq():
    return run_adjust_freq() == 709


def run_adjust_freq():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        return adjust_freq(
            [
                int(x)
                for x in f.read().splitlines()
                if x
            ]
        )


def adjust_freq(inputs):
    checked = []
    freq = 0
    idx = 0
    while freq not in checked:
        checked.append(freq)
        change = inputs[idx]
        freq += change
        if idx >= len(inputs) - 1:
            idx = 0
        else:
            idx += 1

    return freq
