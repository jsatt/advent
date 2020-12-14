import re


FILENAME = 'test_input_p2.txt'
FILENAME = 'input.txt'


def read_input():
    with open(FILENAME) as f:
        return f.readlines()


def apply_mask(mask, val):
    combos = [list(reversed(val)) + (['0'] * (36 - len(val)))]
    for idx, mask_bit in mask.items():
        if mask_bit == '1':
            for combo in combos:
                combo[idx] = '1'
        elif mask_bit == 'X':
            new_combos = []
            for combo in combos:
                combo[idx] = '0'
                new_combos.append(combo.copy())
                combo[idx] = '1'
                new_combos.append(combo.copy())
            combos = new_combos
    return [int(''.join(reversed(x)), base=2) for x in combos]



def process_inst(lines):
    mem = {}
    mask = None
    for line in lines:
        inst, base_addr, val =  re.match('(mask|mem)(?:\[(\d+)\])? = ([\dX]+)', line).groups()
        if inst == 'mask':
            mask = dict((i, v) for i, v in enumerate(reversed(val)))
        else:
            for addr in apply_mask(mask, bin(int(base_addr)).replace('0b', '')):
                mem[addr] = val
    return mem


def p2():
    lines = read_input()
    mem = process_inst(lines)
    return sum(int(x) for x in mem.values())

