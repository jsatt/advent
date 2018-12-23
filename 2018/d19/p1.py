import operator
import os

## sample
INPUT_FILE = 'test_input.txt'
INITIAL_STATE = [0, 0, 0, 0, 0, 0]
ANSWER = 6


## Part 1
# INPUT_FILE = 'input.txt'
# INITIAL_STATE = [0, 0, 0, 0, 0, 0]
# ANSWER = 1464


## Part 2
INPUT_FILE = 'input.txt'
INITIAL_STATE = [1, 0, 0, 0, 0, 0]
# INITIAL_STATE = [1, True, 2, 10551374, 10551374, 10551374]
# INITIAL_STATE = [0, False, 9, 10551374, 1, 10551374]
ANSWER = 1464
# 10551375 too low


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    ip, instructions = parse_instructions(lines)
    state = INITIAL_STATE.copy()
    rounds = 0
    # print(ip, state)
    while state[ip] < len(instructions):
        op = instructions[state[ip]]
        # print(state, op, end='')
        state = OPS[op[0]](op, state)
        print(state)
        state[ip] += 1
        # rounds += 1
        if rounds > 0:
            break
        if state[5] > state[3]:
            rounds += 1
    return state[0]
    # return start, instructions


def parse_instructions(lines):
    start = int(lines[0].split()[1])
    instructions = []
    for line in lines[1:]:
        cmd, a, b, c = line.split()
        instructions.append((cmd, int(a), int(b), int(c)))
    return start, instructions


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


