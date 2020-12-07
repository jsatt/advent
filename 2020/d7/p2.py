import re


def read_input(test=False):
    if test:
        filename = 'test_input_2.txt'
    else:
        filename = 'input.txt'

    with open(filename) as f:
        return f.readlines()


def parse_inst(lines):
    bags = {}
    for line in lines:
        bag, contents = re.match(r'(\w+ \w+) bags contain (.+)', line).groups()
        bags[bag] = {b: int(c) for c, b in re.findall(r'(\d+) (\w+ \w+) bags?[,.]', contents)}
    return bags


def walk_contained_bags(bags, target):
    count = 0
    for bag, cont_count in bags[target].items():
        count += cont_count * (1 + walk_contained_bags(bags, bag))
    return count


def p2(test=False):
    inst = read_input(test=test)
    bags = parse_inst(inst)
    return walk_contained_bags(bags, 'shiny gold')

