## Part 1
ANSWER = 10846352


def test_day():
    return run_day() == ANSWER


def run_day():
    return reverse_engineered_function()


def reverse_engineered_function():
    # r0 = 0
    # ip = 0
    r2 = 0
    # r3 = 0
    r4 = 0
    r5 = 0
    while True:
        # r5 = 123  # 1
        # r5 &= 456  # 2
        # if r5 == 72:  # 3, 4, 5
        # r5 = 0  # 6
        r2 = r5 | 65536  # 7
        r5 = 7571367  # 8
        while True:
            r4 = r2 & 255  # 9
            r5 += r4  # 10
            r5 &= 16777215  # 11
            r5 *= 65899  # 12
            r5 &= 16777215  # 13

            if 256 > r2:  # 14
                # ip += r4  # 15
                # ip += 1  # 16
                # GOTO ip = 28  # 17
                return r5  # 28

            r2 = r2 // 256  # 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
            # r4 = 0  # 18
            # # r3 = 1 # r3 = r4 + 1  # 19
            # # r3 = 256  # r3 *= 256  # 20
            # if 256 > r2:  # r3 = r3 > r2  # 21
                # # ip += r3  # 22
                # # ip += 1  # 23
                # # goto 25 #ip = 25  # 24
                # ip = 17  # 26
            # else:  # r4 += 1  # 25
                # r2 = 1  # r2 = r4  # 27
            # r4 = r5 == r0  # 29
            # ip += r4  # 30
            # ip = 5  # 31
