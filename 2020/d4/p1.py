import re


def read_passports(test=False):
    if test:
        filename = 'test_input_p2_2.txt'
    else:
        filename = 'input.txt'

    with open(filename) as f:
        return f.read().replace('\n\n', ';').replace('\n', ' ').split(';')


def parse_passport(line):
    return dict(p.split(':') for p in line.split(' '))


def basic_check(passport):
    required_fields = ['byr', 'ecl', 'eyr', 'hcl', 'hgt', 'iyr', 'pid']
    return all((f in passport) for f in required_fields)


def full_check(passport):
    try:
        return all([
            check_byr(passport['byr']),
            check_iyr(passport['iyr']),
            check_eyr(passport['eyr']),
            check_hgt(passport['hgt']),
            check_hcl(passport['hcl']),
            check_ecl(passport['ecl']),
            check_pid(passport['pid']),
        ])
    except KeyError:
        return None


def check_byr(val):
    return 1920 <= int(val) <= 2002


def check_iyr(val):
    return 2010 <= int(val) <= 2020


def check_eyr(val):
    return 2020 <= int(val) <= 2030


def check_hgt(val):
    match = re.match('^(\d+)(\w\w)$', val)
    if match:
        dis, unit = match.groups()
        dis = int(dis)
        if unit == 'cm':
            return 150 <= dis <= 193
        else:
            return 59 <= dis <= 76


def check_hcl(val):
    return re.match('^#[0-9a-f]{6}$', val)


def check_ecl(val):
    return val in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def check_pid(val):
    return re.match('^\d{9}$', val)


def p1(test=False):
    lines = read_passports(test=test)
    passports = [parse_passport(l.strip()) for l in lines]
    valid = [p for p in passports if basic_check(p)]
    return len(valid)


def p2(test=False):
    lines = read_passports(test=test)
    passports = [parse_passport(l.strip()) for l in lines]
    valid = [p for p in passports if full_check(p)]
    print([p.get('pid') for p in passports if not check_pid(p.get('pid', ''))])
    print([p.get('pid') for p in passports if check_pid(p.get('pid', ''))])
    return len(valid)
