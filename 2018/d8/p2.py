import os


# INPUT_FILE = 'test_input.txt'
INPUT_FILE = 'input.txt'


def test_day():
    return run_day() == 27490


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        entries = [int(x) for x in f.read().split()]

    tree, _ = parse_entries(entries)
    return tree.get_value()


class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

    def add_child(self, child):
        self.children.append(child)

    def update_metadata(self, data):
        self.metadata = data

    def sum_metadata(self):
        total = sum(self.metadata)
        for child in self.children:
            total += child.sum_metadata()
        return total

    def get_value(self):
        if self.children:
            total = 0
            for val in self.metadata:
                if val == 0 or val > len(self.children):
                    continue
                total += self.children[val - 1].get_value()
            return total
        else:
            return sum(self.metadata)


def parse_entries(entries):
    nodes_count, meta_count = entries[:2]
    data = entries[2:]
    node = Node()
    for _ in range(nodes_count):
        tree, data = parse_entries(data)
        node.add_child(tree)

    node.update_metadata(data[:meta_count])
    return node, data[meta_count:]
