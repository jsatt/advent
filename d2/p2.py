
def calc_ribbon(inp):
    total = 0

    for dim in inp.splitlines():
        h, w, l = [float(x) for x in dim.split('x')]
        vol = l * w * h
        longest = max(h, w, l)
        wrap = (h + w + l - longest) * 2
        total += wrap + vol

    return total

