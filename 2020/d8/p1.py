def read_input(test=False):
    if test:
        filename = 'test_input.txt'
    else:
        filename = 'input.txt'

    with open(filename) as f:
        return f.readlines()


def parse_inst(line):
    inst, val = line.split(' ')
    return inst, int(val)


def walk(inst):
    cur = 0
    acc = 0
    visited_inst = set()
    inst_count = len(inst)

    while cur < inst_count:
        i, v = inst[cur]
        visited_inst.add(cur)
        if i == 'acc':
            acc += v
            cur += 1
        elif i == 'jmp':
            cur += v
        elif i == 'nop':
            cur += 1

        if cur in visited_inst:
            return False, acc

    return True, acc


def p1(test=False):
    lines = read_input(test=test)
    inst = [parse_inst(l) for l in lines]
    return walk(inst)[1]


def p2(test=False):
    lines = read_input(test=test)
    inst = [parse_inst(l) for l in lines]
    swp_cur = 0
    inst_count = len(inst)
    while swp_cur < inst_count:
        while inst[swp_cur][0] not in ['jmp', 'nop']:
            swp_cur += 1
        inst_copy = inst.copy()
        swp = inst_copy[swp_cur]
        if swp[0] == 'jmp':
            inst_copy[swp_cur] = ('nop', swp[1])
        elif swp[0] == 'nop':
            inst_copy[swp_cur] = ('jmp', swp[1])
        comp, acc = walk(inst_copy)
        if comp:
            return acc
        swp_cur += 1
