from typing import List, Tuple


def get_trench_bounds(test: bool = False) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if test:
        target = 'target area: x=20..30, y=-10..-5'
    else:
        target = 'target area: x=244..303, y=-91..-54'

    xrange, yrange = tuple(
        tuple(int(v) for v in b.split('=')[1].split('..'))
        for b in target.split(':')[1].split(',')
    )
    return xrange, yrange


def track_shot(
        trajectory: Tuple[int, int],
        trench_bounds: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, List[Tuple[int, int]]]:
    path: List[Tuple[int, int]] = [(0, 0)]
    pos = path[0]
    hit = False
    while pos[0] < trench_bounds[0][1] and pos[1] > trench_bounds[1][0]:
        pos = (
            pos[0] + trajectory[0],
            pos[1] + trajectory[1],
        )
        path.append(pos)
        trajectory = (
            trajectory[0] + (1 if trajectory[0] < 0 else -1 if trajectory[0] > 0 else 0),
            trajectory[1] - 1
        )

        if (trench_bounds[0][0] <= pos[0] <= trench_bounds[0][1]
            and trench_bounds[1][0] <= pos[1] <= trench_bounds[1][1]):
            hit = True
            break

    return hit, path


def find_highest_trajectory(trench_bounds: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, int]:
    hits = 0
    highest = trench_bounds[1][0]
    for xidx in range(trench_bounds[0][1] + 1):
        for yidx in range(trench_bounds[1][0], -trench_bounds[1][0] + 1):
            hit, path = track_shot((xidx, yidx), trench_bounds)
            if hit:
                highpoint = max([y for _, y in path])
                hits += 1
                if highpoint > highest:
                    highest = highpoint
    return highest, hits


def part_1(test: bool = False) -> int:
    trench_bounds = get_trench_bounds(test=test)
    highest_point, _ = find_highest_trajectory(trench_bounds)
    return highest_point

def part_2(test: bool = False) -> int:
    trench_bounds = get_trench_bounds(test=test)
    _, hits = find_highest_trajectory(trench_bounds)
    return hits

