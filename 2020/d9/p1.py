FILENAME = 'test_input.txt'
PREAMBLE_LEN = 5
# FILENAME = 'input.txt'
# PREAMBLE_LEN = 25


def read_input():
    with open(FILENAME) as f:
        return [int(i) for i in f.readlines()]


def find_sum(nums, target):
    for c1 in nums[:-1]:
        for c2 in nums[0:]:
            if c1 + c2 == target:
                return True

def find_invalid(nums):
    cur = 0
    for target in nums[PREAMBLE_LEN:]:
        search_nums = nums[cur:(cur + PREAMBLE_LEN + 1)]
        if not find_sum(search_nums, target):
            return target
        cur += 1


def find_contiguous_sum(nums, target):
    cur1 = 0
    cur2 = 1
    num_len = len(nums)
    while cur1 < num_len - 1 or cur2 < num_len:
        cont_sum = sum(nums[cur1:cur2 + 1])
        if cont_sum == target:
            return nums[cur1: cur2 + 1]
        elif cont_sum < target:
            cur2 += 1
        elif cont_sum > target:
            cur1 += 1

def p1():
    nums = read_input()
    return find_invalid(nums)


def p2():
    nums = read_input()
    invalid = find_invalid(nums)
    sum_vals = find_contiguous_sum(nums, invalid)
    return min(sum_vals) + max(sum_vals)
