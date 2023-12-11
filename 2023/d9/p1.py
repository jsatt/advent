def read_file(test: bool = False):
    if test:
        file_name = f'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


def find_differences(history):
    seqs = [history]
    while not all(map(lambda x: x == 0, seqs[-1])):
        new_seq = []
        old_seq = seqs[-1]
        seq_len = len(old_seq)
        for idx, num in enumerate(old_seq):
            if idx >= seq_len - 1:
                break
            new_seq.append(old_seq[idx + 1] - num)
        seqs.append(new_seq)
    return seqs


def extrapolate(seqs, reverse=False):
    prev_num = 0
    for idx, seq in enumerate(reversed(seqs)):
        if idx == 0:
            continue
        if reverse:
            prev_num = seq[0] - prev_num
        else:
            prev_num = seq[-1] + prev_num
    return prev_num


def part_1(test=False):
    output = 0
    for line in read_file(test=test):
        seqs = find_differences(list(map(int, line.split())))
        output += extrapolate(seqs)

    return output


def part_2(test=False):
    output = 0
    for line in read_file(test=test):
        seqs = find_differences(list(map(int, line.split())))
        output += extrapolate(seqs, reverse=True)

    return output
