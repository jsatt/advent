
def calc_paper(inp):
    total = 0

    for dim in inp.splitlines():
        h, w, l = [float(x) for x in dim.split('x')]
        s1 = h * w
        s2 = h * l
        s3 = l * w
        smallest = min(s1, s2, s3)
        total += (s1 + s2 + s3) * 2 + smallest

    return total

