INPUT = [0, 3, 6]  # 436, 175594
# INPUT = [1, 3, 2]  # 1, 2578
# INPUT = [2, 1, 3]  # 10, 3544142
# INPUT = [1, 2, 3]  # 27, 261214
# INPUT = [2, 3, 1]  # 78, 6895259
# INPUT = [3, 2, 1]  # 438, 18
# INPUT = [3, 1, 2]  # 1836, 362
INPUT = [1, 20, 8, 12, 0, 14]


def play_game(history, cycles):
    num = 0
    turn = len(INPUT) + 1
    while turn < cycles:
        last_num = num
        if last_num in history:
            last_occur = history[num]
            num = turn - last_occur
        else:
            num = 0
        history[last_num] = turn
        turn += 1
    return num


def p1():
    history = dict((n, i + 1) for i, n in enumerate(INPUT))
    return play_game(history, 2020)


def p2():
    history = dict((n, i + 1) for i, n in enumerate(INPUT))
    return play_game(history, 30000000)


