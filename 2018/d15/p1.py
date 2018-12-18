import os

## sample 1
INPUT_FILE = 'test_input1.txt'
ANSWER = 27730

## sample 2
# INPUT_FILE = 'test_input2.txt'
# ANSWER = 36334

## sample 3
# INPUT_FILE = 'test_input3.txt'
# ANSWER = 39514

## sample 4
# INPUT_FILE = 'test_input4.txt'
# ANSWER = 27755

## sample 5
# INPUT_FILE = 'test_input5.txt'
# ANSWER = 28944

## sample 6
# INPUT_FILE = 'test_input6.txt'
# ANSWER = 18740

## Part 1
# INPUT_FILE = 'input.txt'
# ANSWER = 3337


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        board, units = parse_map(f.read().splitlines())

    rounds = 0
    while True:
        print('')
        print('')
        print('')
        print('round: {}'.format(rounds))
        board.render(units)
        for unit in sort_units(units):
            if unit.is_alive:
                if not any(unit.targets(units)):
                    return rounds * sum([u.hit_points for u in units if u.is_alive])
                target = unit.get_attack_target(units)
                if target:
                    unit.attack(target)
                else:
                    unit.move(board, units)

        units = [u for u in units if u.is_alive]
        for unit in units:
            print('{}{} - {}hp'.format(unit.type, (unit.x, unit.y), unit.hit_points))
        rounds += 1
        if rounds > 50:
            break

    board.render(units)
    return board, units



def parse_map(lines):
    board = Board()
    units = []
    for yidx, line in enumerate(lines):
        for xidx, char in enumerate(line):
            if char != '#':
                space = board.add_space(xidx, yidx)
                if char in 'EG':
                    units.append(Unit(xidx, yidx, char))
        if xidx >= board.width:
            board.width = xidx + 1
    if yidx >= board.height:
        board.height = yidx + 1
    return board, units


def sort_units(units):
    return sorted(units, key=lambda u: (u.y, u.x))


def units_by_coords(units):
    return {(u.x, u.y): u for u in units}


class Space:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = set()
        self.reset()

    def reset(self):
        self.check = 0
        self.score = None
        self.previous = None

    def __repr__(self):
        return '<Space: {}, {}>'.format((self.x, self.y), self.score)


class Board:
    def __init__(self):
        self.spaces = {}
        self.width = 0
        self.height = 0

    def add_space(self, x, y):
        space = Space(x, y)
        self.spaces[x, y] = space
        self.add_edge(space, x - 1, y)
        self.add_edge(space, x + 1, y)
        self.add_edge(space, x, y - 1)
        self.add_edge(space, x, y + 1)
        return space

    def add_edge(self, space, target_x, target_y):
        target = self.spaces.get((target_x, target_y))
        if target:
            target.edges.add(space)
            space.edges.add(target)

    def render(self, units):
        unit_coords = units_by_coords(units)
        for yidx in range(self.height):
            for xidx in range(self.width):
                space = self.spaces.get((xidx, yidx))
                if not space:
                    print('#', end='')  # noqa
                elif (xidx, yidx) in unit_coords:
                    print(unit_coords[xidx, yidx].type, end='')  # noqa
                else:
                    print('.', end='')  # noqa
            print('')

    def get_path(self, start_unit, target_unit, units):
        for space in self.spaces.values():
            space.reset()
        start_space = self.spaces[start_unit.x, start_unit.y]
        start_space.score = 0
        unit_coords = units_by_coords(units)
        queue = [start_space]
        while len(queue) > 0:
            space = queue.pop()
            for edge in sorted(space.edges, key=lambda s: (s.y, s.x)):
                unit = unit_coords.get((edge.x, edge.y))
                if not unit or not unit.is_alive:
                    if edge.score is None or edge.score > space.score + 1:
                        edge.previous = space
                        edge.score = space.score + 1
                        queue.append(edge)

        target = self.spaces[target_unit.x, target_unit.y]
        paths = sorted([
            e
            for e in target.edges
            if e.previous
        ], key=lambda s: (s.score, s.y, s.x))
        if paths:
            current = paths[0]
            while current.previous and current.previous != start_space:
                current = current.previous
            return current, paths[0].score
        return None, None


class Unit:
    attack_power = 3
    hit_points = 200

    def __init__(self, x, y, unit_type):
        self.x = x
        self.y = y
        self.type = unit_type
        self.target_type = 'E' if unit_type == 'G' else 'G'

    def take_hit(self, attack):
        self.hit_points -= attack

    @property
    def is_alive(self):
        return self.hit_points > 0

    def targets(self, units):
        return [
            u
            for u in units
            if u.type == self.target_type and u.is_alive
        ]

    def get_attack_target(self, units):
        unit_coords = units_by_coords(units)
        adjacents = [
            unit_coords.get((self.x - 1, self.y)),
            unit_coords.get((self.x + 1, self.y)),
            unit_coords.get((self.x, self.y - 1)),
            unit_coords.get((self.x, self.y + 1)),
        ]
        targets = [
            u for u in adjacents
            if u and u.type == self.target_type and u.is_alive
        ]
        if any(targets):
            return sorted(targets, key=lambda u: u.hit_points)[0]

    def attack(self, target):
        print('{}{} attacks {}{}'.format(self.type, (self.x, self.y), target.type, (target.x, target.y)))
        target.take_hit(self.attack_power)

    def move(self, board, units):
        shortest_path = None
        shortest_dist = 0
        for target in self.targets(units):
            path, distance = board.get_path(self, target, units)
            if path and distance and (shortest_path is None or distance < shortest_dist):
                shortest_path = path
        if shortest_path:
            self.x = shortest_path.x
            self.y = shortest_path.y

    def __repr__(self):
        return '<Unit: {}; {}>'.format(self.type, (self.x, self.y))
