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

    regular_sleeper = sorted(lines.items(), key=lambda x: max(x[1]['min_distro']), reverse=True)[0]
    common_min = regular_sleeper[1]['min_distro'].index(max(regular_sleeper[1]['min_distro']))

    return int(regular_sleeper[0]) * common_min


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
                idx = sleep_time.minute
                while idx < time.minute:
                    guards[current_guard]['min_distro'][idx] += 1
                    idx += 1
                sleep_time = None
        else:
            current_guard = re.compile('Guard #(\d+) begins shift').search(msg).group(1)
            if current_guard not in guards:
                guards[current_guard] = {'total': 0, 'min_distro': [0] * 60}
    return guards
