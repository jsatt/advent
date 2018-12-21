import operator
import os
import re

INPUT_FILE = 'input.txt'
ANSWER = 496


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    samples, inputs = parse_input(lines)
    codes = process_samples(samples)
    return process_input(codes, inputs)


def parse_input(lines):
    samples = []
    inputs = []
    line_iter = iter(lines)
    for line in line_iter:
        if line.startswith('Before: '):
            samples.append([
                parse_sample(line),
                [int(x) for x in next(line_iter).split()],
                parse_sample(next(line_iter))
            ])
        elif line:
            inputs.append([int(x) for x in line.split()])
    return samples, inputs


def parse_sample(line):
    pattern = re.compile('[(Before:)|(After: )] \[(\d), (\d), (\d), (\d)\]')
    return [int(x) for x in pattern.search(line).groups()]


def calc(inp, a, b, c, op):
    out = inp[::]
    out[c] = op(a, b)
    return out


OPS = {
    'addr': lambda ops, inp: calc(inp, inp[ops[1]], inp[ops[2]], ops[3], operator.add),
    'addi': lambda ops, inp: calc(inp, inp[ops[1]], ops[2], ops[3], operator.add),
    'mulr': lambda ops, inp: calc(inp, inp[ops[1]], inp[ops[2]], ops[3], operator.mul),
    'muli': lambda ops, inp: calc(inp, inp[ops[1]], ops[2], ops[3], operator.mul),
    'banr': lambda ops, inp: calc(inp, inp[ops[1]], inp[ops[2]], ops[3], operator.and_),
    'bani': lambda ops, inp: calc(inp, inp[ops[1]], ops[2], ops[3], operator.and_),
    'borr': lambda ops, inp: calc(inp, inp[ops[1]], inp[ops[2]], ops[3], operator.or_),
    'bori': lambda ops, inp: calc(inp, inp[ops[1]], ops[2], ops[3], operator.or_),
    'setr': lambda ops, inp: calc(inp, inp[ops[1]], 0, ops[3], operator.add),
    'seti': lambda ops, inp: calc(inp, ops[1], 0, ops[3], operator.add),
    'gtir': lambda ops, inp: calc(inp, ops[1], inp[ops[2]], ops[3], operator.gt),
    'gtri': lambda ops, inp: calc(inp, inp[ops[1]], ops[2], ops[3], operator.gt),
    'gtrr': lambda ops, inp: calc(inp, inp[ops[1]], inp[ops[2]], ops[3], operator.gt),
    'eqir': lambda ops, inp: calc(inp, ops[1], inp[ops[2]], ops[3], operator.eq),
    'eqri': lambda ops, inp: calc(inp, inp[ops[1]], ops[2], ops[3], operator.eq),
    'eqrr': lambda ops, inp: calc(inp, inp[ops[1]], inp[ops[2]], ops[3], operator.eq),
}


def process_samples(samples):
    codes = {code: list(OPS.keys()) for code in range(len(OPS))}
    decided = {}
    for inp, op, out in samples:
        keepers = []
        for name in codes[op[0]]:
            if name not in decided.values() and OPS[name](op, inp) == out:
                keepers.append(name)
        if len(keepers) == 1:
            decided[op[0]] = keepers[0]
            keepers = []
        codes[op[0]] = keepers
    return decided


def process_input(codes, inputs):
    state = [0, 0, 0, 0]
    for op in inputs:
        state = OPS[codes[op[0]]](op, state)
    return state
