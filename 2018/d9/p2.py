from collections import deque
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
LAST_MARBLE = 7083300
ANSWER = 2954067253


def test_day():
    return run_day() == ANSWER


def run_day():
    scores = [0] * PLAYERS
    played = deque([0])
    for marble in range(1, LAST_MARBLE + 1):
        if not marble % 23:
            played.rotate(7)
            scores[marble % PLAYERS] += marble + played.pop()
            played.rotate(-1)
        else:
            played.rotate(-1)
            played.append(marble)

    return max(scores)


