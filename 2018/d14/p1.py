
INITIAL_SCORES = [3, 7]
FINAL_ITERATIONS = 10

# sample 1
# PRACTICE_ITERATIONS = 9
# ANSWER = '5158916779'

# sample 2
# PRACTICE_ITERATIONS = 5
# ANSWER = '0124515891'

# sample 3
# PRACTICE_ITERATIONS = 18
# ANSWER = '9251071085'

# sample 4
# PRACTICE_ITERATIONS = 2018
# ANSWER = '5941429882'

# Part 1
PRACTICE_ITERATIONS = 110201
ANSWER = '6107101544'


def test_day():
    return run_day() == ANSWER


def run_day():
    elf1 = 0
    elf2 = 1
    scores = INITIAL_SCORES.copy()
    while len(scores) < PRACTICE_ITERATIONS + FINAL_ITERATIONS:
        new_score = scores[elf1] + scores[elf2]
        if new_score >= 10:
            scores.append(new_score // 10)
            scores.append(new_score % 10)
        else:
            scores.append(new_score)

        elf1 = new_idx(elf1, scores)
        elf2 = new_idx(elf2, scores)
    return ''.join(str(x) for x in scores[PRACTICE_ITERATIONS:PRACTICE_ITERATIONS + FINAL_ITERATIONS])

def new_idx(idx, scores):
    new = idx + scores[idx] + 1
    while new >= len(scores):
        new = new - len(scores)
    return new
