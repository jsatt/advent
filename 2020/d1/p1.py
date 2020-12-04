target = 2020

def read_report(test=False):
    if test:
        return [
            1721,
            979,
            366,
            299,
            675,
            1456,
        ]
    else:
        with open('input.txt') as f:
            return [int(r) for r in f.readlines()]

def p1(test=False):
    report = read_report(test=test)
    for idx, val in enumerate(report):
        cur = idx + 1
        rlen = len(report)
        while cur < rlen:
            if val + report[cur] == target:
                return val * report[cur]
            cur += 1

def p2(test=False):
    report = read_report(test=test)
    for idx, val in enumerate(report):
        cur1 = idx + 1
        rlen = len(report)
        while cur1 < rlen - 1:
            cur2 = cur1 + 1
            while cur2 < rlen:
                if val + report[cur1] + report[cur2] == target:
                    return val * report[cur1] * report[cur2]
                cur2 += 1
            cur1 += 1
