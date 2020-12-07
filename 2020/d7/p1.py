import re


def read_input(test=False):
    if test:
        filename = 'test_input_1.txt'
    else:
        filename = 'input.txt'

    with open(filename) as f:
        return f.readlines()


def parse_inst(lines):
    bags = {}
    for line in lines:
        contain_bag, contents = re.match(r'(\w+ \w+) bags contain (.+)', line).groups()
        for count, bag in re.findall(r'(\d+) (\w+ \w+) bags?[,.]', contents):
            if bag not in bags:
                bags[bag] ={}
            bags[bag][contain_bag] = count
    return bags

def walk_containing_bags(bags, target):
    containers = set()
    for bag in bags.get(target, []):
        containers.add(bag)
        containers.update(walk_bags(bags, bag))
    return containers


def p1(test=False):
    inst = read_input(test=test)
    bags = parse_inst(inst)
    containing_bags = walk_bags(bags, 'shiny gold')
    return len(containing_bags)
