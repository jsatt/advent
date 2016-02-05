import re
from itertools import chain


class CircuitProcessor:
    def __init__(self):
        self.reset_storage()

    def repeat_circuit(self, lines, times):
        value = self.process_circut(lines)
        for _ in range(times - 1):
            value = self.process_circut(lines, ['{} -> b'.format(value)])
        return value

    def process_circut(self, lines, override=[]):
        self.reset_storage()
        for line in chain(lines.splitlines(), override):
            dest, gate, inputs = self.parse_line(line)
            self.record_command(dest, gate, inputs)
        value = self.get_value('a')
        return value

    def reset_storage(self):
        self.commands = {}
        self.values = {}

    def parse_line(self, line):
        command, dest = line.split(' -> ')
        cmd_parts = command.split(' ')
        inputs = []
        gate = None
        for part in cmd_parts:
            if re.search(r'[A-Z]+', part):
                gate = part
            else:
                inputs.append(part)
        return dest, gate, inputs

    def record_command(self, dest, gate, inputs):
        if gate is None:
            self.values[dest] = inputs[0]
        else:
            self.commands[dest] = (inputs, gate)

    def get_value(self, ref):
        try:
            value = int(ref)
        except ValueError:
            if ref in self.values:
                try:
                    value = int(self.values[ref])
                except ValueError:
                    value = self.get_value(self.values[ref])
            else:
                value = self.calc(*self.commands[ref])
                if value < 0:
                    value = 65536 + value
                self.values[ref] = value
        return value

    def calc(self, values, gate):
        values = list(map(self.get_value, values))
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
