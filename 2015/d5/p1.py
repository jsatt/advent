import re


def test_word(word):
    return (
        not re.match(r'.*(ab|cd|pq|xy).*', word) and
        bool(re.match(r'.*(?P<x>[a-z])(?P=x).*', word)) and
        len([x for x in word if x in 'aeiou']) >= 3
    )


def count_nice(lines):
    count = 0
    for l in lines.splitlines():
        if test_word(l):
            count += 1

    return count
