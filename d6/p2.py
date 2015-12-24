from collections import defaultdict

def handle_lights(inst):
    lights = defaultdict(int)
    for l in inst.splitlines():
        task, start, _, end = l.rsplit(' ', 3)
        x1, y1 = [int(i) for i in start.split(',')]
        x2, y2 = [int(i) for i in end.split(',')]

        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                if task == 'turn on':
                    lights[(x, y)] += 1
                elif task == 'turn off':
                    if lights[(x, y)] > 0:
                        lights[(x, y)] -= 1
                elif task == 'toggle':
                    lights[(x, y)] += 2

    return sum(lights.values())
