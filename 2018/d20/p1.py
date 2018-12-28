
import os


# sample 1
# INPUT_FILE = 'test_input1.txt'
# ANSWER = 3, 0

# sample 1
# INPUT_FILE = 'test_input2.txt'
# ANSWER = 10, 0

# sample 1
# INPUT_FILE = 'test_input3.txt'
# ANSWER = 18, 0

# sample 1
# INPUT_FILE = 'test_input4.txt'
# ANSWER = 23, 0

# sample 1
# INPUT_FILE = 'test_input5.txt'
# ANSWER = 31, 0

# part 1 & 2
INPUT_FILE = 'input.txt'
ANSWER = 3465, 7956


def test_day():
    return run_day() == ANSWER


def run_day():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        line = f.read().splitlines()[0]

    building = Building()
    building.parse_directions(line)
    # building.render()
    building.calculate_distance(building.rooms[0, 0])
    scores = [r.score for r in building.rooms.values()]
    return sorted(scores, reverse=True)[0], len([s for s in scores if s >= 1000])


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.adjacent_rooms = set()
        self.reset()

    def reset(self):
        self.check = 0
        self.score = None
        self.visited = False

    def __repr__(self):
        return '<Room: {}, {}>'.format((self.x, self.y), self.score)


class Building:
    def __init__(self):
        self.rooms = {}
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0

    def add_room(self, x, y):
        room = Room(x, y)
        self.rooms[x, y] = room
        if x > self.max_x:
            self.max_x = x
        elif x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        elif y < self.min_y:
            self.min_y = y
        return room

    def add_door(self, room, direction):
        target_x = room.x
        target_y = room.y
        if direction == 'N':
            target_y -= 1
        elif direction == 'S':
            target_y += 1
        elif direction == 'E':
            target_x += 1
        elif direction == 'W':
            target_x -= 1
        target = self.rooms.get((target_x, target_y))
        if not target:
            target = self.add_room(target_x, target_y)
            self.rooms[target_x, target_y] = target
        room.adjacent_rooms.add(target)
        target.adjacent_rooms.add(room)
        return target

    def render(self):
        print('#' + ('#' * ((self.max_x - self.min_x + 1) * 2)))
        for yidx in range(self.min_y, self.max_y + 1):
            print('#', end='')
            next_row = '#'
            for xidx in range(self.min_x, self.max_x + 1):
                if xidx == 0 and yidx == 0:
                    print('X', end='')
                else:
                    print('.', end='')
                if (xidx, yidx) in self.rooms:
                    room = self.rooms[xidx, yidx]
                    adjacents = [(a.x, a.y) for a in room.adjacent_rooms]
                    if (room.x + 1, room.y) in adjacents:
                        print('|', end='')
                    else:
                        print('#', end='')
                    if (room.x, room.y + 1) in adjacents:
                        next_row += '-'
                    else:
                        next_row += '#'
                    next_row += '#'
                else:
                    print('#', end='')
                    next_row += '#'

            print('')
            print(next_row)

    def parse_directions(self, directions):
        first_room = self.add_room(0, 0)
        self.parse_segment(first_room, directions)

    def parse_segment(self, parent, directions):
        current_room = parent
        direct_iter = iter(directions)
        for direction in direct_iter:
            if direction in '^$':
                pass
            elif direction in 'NSEW':
                current_room = self.add_door(current_room, direction)
            elif direction == '(':
                segment = ''
                branches = []
                parens = []
                for segment_dir in direct_iter:
                    # if segment_dir == '|':
                    if not parens and segment_dir == ')':
                        branches.append(segment)
                        # import pdb; pdb.set_trace()  # XXX BREAKPOINT
                        for branch in branches:
                            self.parse_segment(current_room, branch)
                        break
                    elif not parens and segment_dir == '|':
                        branches.append(segment)
                        segment = ''
                    else:
                        segment += segment_dir
                        if segment_dir == '(':
                            parens.append(segment_dir)
                        elif segment_dir == ')':
                            parens.pop()

    def calculate_distance(self, initial_room):
        initial_room.score = 0
        queue = [initial_room]
        while queue:
            current_room = queue.pop()
            for room in current_room.adjacent_rooms:
                if room.score is None or room.score > current_room.score + 1:
                    room.score = current_room.score + 1
                    queue.append(room)
