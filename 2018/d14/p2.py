
INITIAL_SCORES = [3, 7]

# sample 1
# SEQUENCE = '51589'
# ANSWER = 9

# sample 2
# SEQUENCE = '01245'
# ANSWER = 5

# sample 3
# SEQUENCE = '92510'
# ANSWER = 18

# sample 4
# SEQUENCE = '59414'
# ANSWER = 2018

# Part 2
SEQUENCE = '110201'
ANSWER = 20291131

def test_day():
    return run_day() == ANSWER


def run_day():
    elf1 = 0
    elf2 = 1
    scores = ''.join(str(x) for x in INITIAL_SCORES.copy())
    while True:
        scores += str(int(scores[elf1]) + int(scores[elf2]))
        if SEQUENCE in scores[-len(SEQUENCE) * 2:]:
            return scores.index(SEQUENCE)

        elf1 = new_idx(elf1, scores)
        elf2 = new_idx(elf2, scores)

def new_idx(idx, scores):
    new = idx + int(scores[idx]) + 1
    return new % len(scores)
