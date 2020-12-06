def read_input(test=False):
    if test:
        filename = 'test_input.txt'
    else:
        filename = 'input.txt'
    with open(filename) as f:
        return [l.strip().split('\n') for l in f.read().split('\n\n')]


def p1(test=False):
    groups = read_input(test=test)
    sums = 0
    for group in groups:
        answers = set()
        for p in group:
            answers |= set(p)
        sums += len(answers)
    return sums


def p2(test=False):
    groups = read_input(test=test)
    sums = 0
    for group in groups:
        answers = set(group[0].strip())
        for p in group[0:]:
            answers = answers.intersection(set(p))
        sums += len(answers)
    return sums
