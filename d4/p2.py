from hashlib import md5


def calc_coin(key):
    val = ''
    i = 0

    while not md5('{}{}'.format(key, i).encode('utf8')).hexdigest().startswith('000000'):
        i += 1

    return i
