from datetime import datetime
import os
import re


def test_schedule():
    return run_schedule() == 125444


def run_schedule():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        lines = parse_schedule(f.read().splitlines())

    sleepiest = sorted(lines.items(), key=lambda x: x[1]['total'], reverse=True)[0]
    min_distro = factor_times(sleepiest[1]['times'])
    common_min = min_distro.index(max(min_distro))

    return int(sleepiest[0]) * common_min


def parse_schedule(inputs):
    regex = re.compile('\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.*)')
    inputs.sort()
    guards = {}
    current_guard = None
    sleep_time = None
    for line in inputs:
        timestamp, msg = regex.search(line).groups()
        time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M')
        if msg == 'falls asleep':
            sleep_time = time
        elif msg == 'wakes up':
            if sleep_time:
                time_diff = (time - sleep_time).seconds // 60
                guards[current_guard]['total'] += time_diff
                guards[current_guard]['times'].append((sleep_time, time))
            sleep_time = None
        else:
            current_guard = re.compile('Guard #(\d+) begins shift').search(msg).group(1)
            if current_guard not in guards:
                guards[current_guard] = {'total': 0, 'times': []}
    return guards


def factor_times(times):
    mins = [0] * 60
    for start, end in times:
        idx = start.minute
        while idx < end.minute:
            mins[idx] += 1
            idx += 1
    return mins
