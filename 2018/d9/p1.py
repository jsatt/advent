## sample 1
# PLAYERS = 9
# LAST_MARBLE = 25
# ANSWER = 32
## sample 2
# PLAYERS = 10
# LAST_MARBLE = 1618
# ANSWER = 8317
## sample 3
# PLAYERS = 13
# LAST_MARBLE = 7999
# ANSWER = 146373
## sample 4
# PLAYERS = 17
# LAST_MARBLE = 1104
# ANSWER = 2764
## sample 5
# PLAYERS = 21
# LAST_MARBLE = 6111
# ANSWER = 54718
## sample 6
# PLAYERS = 30
# LAST_MARBLE = 5807
# ANSWER = 37305

PLAYERS = 486
LAST_MARBLE = 70833
ANSWER = 373597


def test_day():
    return run_day() == ANSWER


def run_day():
    scores = [0] * PLAYERS
    played = [0]
    score_idx = 0
    pos = 1
    for marble in range(1, LAST_MARBLE + 1):
        if not marble % 23:
            bonus_idx = pos - 7
            if bonus_idx < 0:
                bonus_idx = len(played) + bonus_idx
            scores[score_idx] += marble + played.pop(bonus_idx)
            pos = bonus_idx
        else:
            pos += 2
            if pos > len(played):
                pos = 1
            played.insert(pos, marble)
        if score_idx >= PLAYERS - 1:
            score_idx = 0
        else:
            score_idx += 1

    return max(scores)

