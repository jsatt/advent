import re


def read_input(test=False):
    if test:
        return [
            '1-3 a: abcde',
            '1-3 b: cdefg',
            '2-9 c: ccccccccc',
        ]
    else:
        with open('input.txt') as f:
            return f.readlines()


def parse_line(line):
    dig1, dig2, char, passwd = re.match(r'(\d+)-(\d+) (\w): (\w+)', line).groups()
    return int(dig1), int(dig2), char, passwd


def char_count(passwd):
    counts = {}
    for char in passwd:
        if char in counts:
            counts[char] += 1
        else:
            counts[char] = 1
    return counts


def test_line(line):
    omin, omax, char, passwd = parse_line(line)
    charcnt = char_count(passwd)
    return omin <= charcnt.get(char, 0) <= omax


def p1(test=False):
    lines = read_input(test=test)
    matches = 0
    for line in lines:
        if test_line(line):
            matches += 1

    return matches

def p2(test=False):
    matches = 0
    for line in read_input(test=test):
        pos1, pos2, char, passwd = parse_line(line)
        char1 = passwd[pos1 - 1]
        char2 = passwd[pos2 - 1]
        if char1 != char2 and (char1 == char or char2 == char):
            matches += 1
    return matches
