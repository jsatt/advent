import re


def test_word(word):
    return (
        bool(re.match(r'.*(?P<x>[a-z]).{1}(?P=x).*', word)) and
        bool(re.match(r'.*(?P<x>[a-z]{2}).*(?P=x).*', word))
    )


def count_nice(lines):
    count = 0
    for l in lines.splitlines():
        if test_word(l):
            count += 1

    return count
