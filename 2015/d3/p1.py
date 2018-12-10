def process_directions(dirs):
    visited = {(0, 0): True}
    current_pos = 0, 0
    for d in dirs:
        if d == '^':
            current_pos = current_pos[0] + 1, current_pos[1]
        elif d == 'v':
            current_pos = current_pos[0] - 1, current_pos[1]
        elif d == '>':
            current_pos = current_pos[0], current_pos[1] + 1
        elif d == '<':
            current_pos = current_pos[0], current_pos[1] - 1

        visited[current_pos] = True

    return len(visited.keys())
