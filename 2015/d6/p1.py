from collections import defaultdict

def handle_lights(inst):
    lights = defaultdict(bool)
    for l in inst.splitlines():
        task, start, _, end = l.rsplit(' ', 3)
        x1, y1 = [int(i) for i in start.split(',')]
        x2, y2 = [int(i) for i in end.split(',')]

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if task == 'turn on':
                    lights[(x, y)] = True
                elif task == 'turn off':
                    lights[(x, y)] = False
                elif task == 'toggle':
                    lights[(x, y)] = not lights[(x, y)]

    return len([i for i in lights.values() if i])
