from math import prod


FILENAME = 'test_input.txt'
FILENAME = 'input.txt'



def read_input():
    with open(FILENAME) as f:
        return [list(l.strip().replace(' ','')) for l in f.readlines()]


def evaluate(group):
    group_iter = iter(group)
    running = 0
    op = sum
    for char in group_iter:
        if char == '(':
            group = []
            parens = []
            for inner in group_iter:
                if inner == ')' and not parens:
                    running = op([running, evaluate(group)])
                    break
                else:
                    group.append(inner)
                    if inner == '(':
                        parens.append(inner)
                    elif inner == ')':
                        parens.pop()
        elif char == '+':
            op = sum
        elif char == '*':
            op = prod
        else:
            if not running:
                running = int(char)
            else:
                running = op([running, int(char)])
    return running


def p1():
    lines = read_input()
    evals = [evaluate(l) for l in lines]
    print(evals)
    return sum(evals)
