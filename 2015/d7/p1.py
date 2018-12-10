import re

commands = {}
values = {}


def process_circut(lines):
    for line in lines.splitlines():
        command, dest = line.split(' -> ')
        cmd_parts = command.split(' ')
        inputs = []
        gate = None
        for part in cmd_parts:
            if re.search(r'[A-Z]+', part):
                gate = part
            else:
                inputs.append(part)
        if gate is None:
            values[dest] = inputs[0]
        else:
            commands[dest] = (inputs, gate)

    return get_value('a')


def get_value(ref):
    try:
        value = int(ref)
    except ValueError:
        if ref in values:
            try:
                value = int(values[ref])
            except ValueError:
                value = get_value(values[ref])
        else:
            value = calc(*commands[ref])
            if value < 0:
                value = 65536 + value
            values[ref] = value
    return value


def calc(values, gate):
    values = list(map(get_value, values))
    if gate == 'NOT':
        return ~ values[0]
    elif gate == 'AND':
        return values[0] & values[1]
    elif gate == 'OR':
        return values[0] | values[1]
    elif gate == 'LSHIFT':
        return values[0] << values[1]
    elif gate == 'RSHIFT':
        return values[0] >> values[1]
    return values[0]
