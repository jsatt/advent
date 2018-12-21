import os

## sample 1
INPUT_FILE = 'test_input1.txt'
ANSWER = 4988
# ANSWER = 27730

## sample 2
# INPUT_FILE = 'test_input2.txt'

## sample 3
# INPUT_FILE = 'test_input3.txt'
# ANSWER = 31284

## sample 4
# INPUT_FILE = 'test_input4.txt'
# ANSWER = 3478

## sample 5
# INPUT_FILE = 'test_input5.txt'
# ANSWER = 6474

## sample 6
# INPUT_FILE = 'test_input6.txt'
# ANSWER = 1140

## Part 2
INPUT_FILE = 'input.txt'
ANSWER = 77872
# 80040 too high
# 35072 too low


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    elf_power = 4
    while True:
        board, units = parse_map(lines, elf_power)
        rounds = 0
        units = sort_units([u for u in units if u.is_alive])
        # board.render(units)
        while True:
            # print('-' * 30)
            # print('Round', rounds + 1, 'power', elf_power)
            try:
                for unit in units:
                    if unit.is_alive:
                        units = sort_units([u for u in units if u.is_alive])
                        if not any(unit.targets(units)):
                            board.render(units)
                            return rounds * sum([u.hit_points for u in units if u.is_alive])
                        target = unit.get_attack_target(units)
                        if not target:
                            unit.move(board, units)
                            target = unit.get_attack_target(units)
                        if target:
                            unit.attack(target)
                    if any([not u.is_alive for u in units if u.type == 'E']):
                        raise ElfDied
            except ElfDied:
                break

            # board.render(units)
            goblins = [u.hit_points for u in units if u.type == 'G']
            elves = [u.hit_points for u in units if u.type == 'E']
            rounds += 1
        elf_power += 1


def parse_map(lines, elf_power):
    board = Board()
    units = []
    for yidx, line in enumerate(lines):
        for xidx, char in enumerate(line):
            if char != '#':
                space = board.add_space(xidx, yidx)
                if char == 'E':
                    units.append(Unit(xidx, yidx, char, elf_power))
                elif char == 'G':
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
        self.visited = False

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
        units = sort_units([u for u in units if u.is_alive])
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
        goblins = [u.hit_points for u in units if u.type == 'G']
        elves = [u.hit_points for u in units if u.type == 'E']
        print(len(goblins), 'goblins remaining:', goblins)
        print(len(elves), 'elves remaining:', elves)

    def get_path(self, start_unit, target_unit, units):
        for space in self.spaces.values():
            space.reset()
        start_space = self.spaces[start_unit.x, start_unit.y]
        start_space.score = 0
        unit_coords = units_by_coords(units)
        queue = [start_space]
        while len(queue) > 0:
            space = queue.pop(0)
            for edge in sorted(space.edges, key=lambda s: (s.y, s.x)):
                unit = unit_coords.get((edge.x, edge.y))
                if not unit or not unit.is_alive:
                    if edge.score is None or edge.score > space.score + 1:
                        edge.score = space.score + 1
                        queue.append(edge)

        target = self.spaces[target_unit.x, target_unit.y]
        paths = sorted([
            e
            for e in target.edges
            if e.score is not None and not unit_coords.get((e.x, e.y))
        ], key=lambda s: (s.score, s.y, s.x))
        if paths:
            current = paths[0]
            while current and not current.visited and start_space not in current.edges:
                current.visited = True
                next_space = sorted([
                    s
                    for s in current.edges
                    if s.score is not None and not s.visited and not unit_coords.get((s.x, s.y))
                ], key=lambda s: (s.score, s.y, s.x))
                if next_space:
                    current = next_space[0]
                else:
                    current = None
            return current, paths[0].score
        return None, None


class Unit:
    hit_points = 200

    def __init__(self, x, y, unit_type, power=3):
        self.x = x
        self.y = y
        self.type = unit_type
        self.attack_power = power
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
            return sorted(targets, key=lambda u: (u.hit_points, u.y, u.x))[0]

    def attack(self, target):
        target.take_hit(self.attack_power)

    def move(self, board, units):
        shortest_path = None
        shortest_dist = 0
        paths = []
        for target in sorted(self.targets(units), key=lambda u: (u.y, u.x)):
            path, distance = board.get_path(self, target, units)
            if path and distance and (shortest_path is None or distance < shortest_dist):
                shortest_path = path
                shortest_dist = distance
            paths.append(path)

        if shortest_path:
            self.x = shortest_path.x
            self.y = shortest_path.y

    def __repr__(self):
        return '<Unit: {}; {}>'.format(self.type, (self.x, self.y))


class ElfDied(Exception):
    pass
