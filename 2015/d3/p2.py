def process_directions(dirs):
    visited = {(0, 0): True}
    santa = 0
    bot = 1
    current_pos = {santa: (0, 0), bot: (0, 0)}
    for i, d in enumerate(dirs):
        x = (i % 2) # even = santa, odd = bot

        if d == '^':
            current_pos[x] = current_pos[x][0] + 1, current_pos[x][1]
        elif d == 'v':
            current_pos[x] = current_pos[x][0] - 1, current_pos[x][1]
        elif d == '>':
            current_pos[x] = current_pos[x][0], current_pos[x][1] + 1
        elif d == '<':
            current_pos[x] = current_pos[x][0], current_pos[x][1] - 1

        visited[current_pos[x]] = True

    return len(visited.keys())
