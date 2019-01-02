## Part 2
ANSWER = 5244670


def test_day():
    return run_day() == ANSWER


def run_day():
    return reverse_engineered_function()


def reverse_engineered_function():
    halts = set()
    r2 = 0
    r4 = 0
    r5 = 0
    last_added = 0
    while True:
        r2 = r5 | 65536
        r5 = 7571367
        while True:
            r4 = r2 & 255
            r5 += r4
            r5 &= 16777215
            r5 *= 65899
            r5 &= 16777215

            if 256 > r2:
                if r5 not in halts:
                    halts.add(r5)
                    print(r5)
                    last_added = r5
                else:
                    return last_added
                break

            r2 = r2 // 256
