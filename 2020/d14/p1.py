import re


# FILENAME = 'test_input_p1.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return f.readlines()


def apply_mask(mask, val):
    bits = list(reversed(val)) + (['0'] * (36 - len(val)))
    for idx, mask_bit in mask.items():
        bits[idx] = mask_bit
    return int(''.join(reversed(bits)), base=2)



def process_inst(lines):
    mem = {}
    mask = None
    for line in lines:
        inst, addr, val =  re.match('(mask|mem)(?:\[(\d+)\])? = ([\dX]+)', line).groups()
        if inst == 'mask':
            mask = dict((i, v) for i, v in enumerate(reversed(val)) if v != 'X')
        else:
            mem[addr] = apply_mask(mask, bin(int(val)).replace('0b', ''))
    return mem


def p1():
    lines = read_input()
    mem = process_inst(lines)
    return sum(mem.values())
