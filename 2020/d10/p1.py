FILENAME = 'test_input_1.txt'
FILENAME = 'test_input_2.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return [int(l) for l in f.readlines()]


def p1():
    adapters = read_input()
    adapters.sort()
    jolts_1 = 0
    jolts_3 = 1  # assume 3 jolt jump in device
    cur_jolt = 0

    for adapter in adapters:
        diff = adapter - cur_jolt
        if diff == 1:
            jolts_1 += 1
        elif diff == 3:
            jolts_3 += 1

        cur_jolt = adapter
    return jolts_1 * jolts_3


def walk(target, max_jolt, values, answers):
    if target not in answers:
        if target == max_jolt - 3:
            return 1

        paths = 0
        for idx, value in enumerate(values):
            if target < value <= target + 3:
                paths += walk(value, max_jolt, values[idx:], answers)
        answers[target] = paths
    return answers[target]


def p2():
    adapters = read_input()
    adapters.sort()
    device_jolt = adapters[-1] + 3
    answers = {}
    walk(0, device_jolt, adapters, answers)
    return answers[0]
