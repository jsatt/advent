from functools import reduce
from operator import mul
from typing import Generator, Tuple, Union

import aiofiles


async def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    async with aiofiles.open(file_name, 'r', encoding='utf8') as f:
        for line in await f.readlines():
            yield line.strip()


async def get_binary_msg(test: bool = False) -> Generator[str, None, None]:
    async for line in read_file(test=test):
        bits = bin(int(line, 16))[2:]
        if (pad_len := len(bits) % 8) != 0:
            padding = '0' * (8 - pad_len)
        else:
            padding = ''
        yield line, padding + bits


def parse_msg(bits: str) -> Tuple[int, int, Union[int, list], str]:
    remaining_bits = bits
    version = int(remaining_bits[:3], 2)
    remaining_bits = remaining_bits[3:]
    type = int(remaining_bits[:3], 2)
    remaining_bits = remaining_bits[3:]
    if type == 4:
        msg = ''
        while True:
            lit_bits = remaining_bits[:5]
            remaining_bits = remaining_bits[5:]
            prefix = lit_bits[0]
            msg += lit_bits[1:]
            if prefix == '0':
                break
        message = int(msg, 2)
    else:
        ltype = remaining_bits[0]
        remaining_bits = remaining_bits[1:]
        if ltype == '0':
            length = int(remaining_bits[:15], 2)
            remaining_bits = remaining_bits[15:]
            packets = remaining_bits[:length]
            remaining_bits = remaining_bits[length:]
            message = []
            while packets:
                v, t, m, packets = parse_msg(packets)
                message.append((v,t,m))
        else:
            length = int(remaining_bits[:11], 2)
            remaining_bits = remaining_bits[11:]
            message = []
            for _ in range(length):
                v, t, m, remaining_bits = parse_msg(remaining_bits)
                message.append((v, t, m))
    return version, type, message, remaining_bits


def sum_versions(message: Tuple[int, int, Union[int, list]]) -> int:
    if isinstance(message[2], int):
        return message[0]
    children = sum([sum_versions(m) for m in message[2]])
    return message[0] + children


def process_message(message: Tuple[int, int, Union[int, list]]) -> int:
    _, type, msg = message
    if type == 0:
        return sum([process_message(m) for m in msg])
    elif type == 1:
        return reduce(mul, [process_message(m) for m in msg])
    elif type == 2:
        return min([process_message(m) for m in msg])
    elif type == 3:
        return max([process_message(m) for m in msg])
    elif type == 5:
        return int(process_message(msg[0]) > process_message(msg[1]))
    elif type == 6:
        return int(process_message(msg[0]) < process_message(msg[1]))
    elif type == 7:
        return int(process_message(msg[0]) == process_message(msg[1]))
    return msg


async def part_1(test: bool = False) -> int:
    async for line, bits in get_binary_msg(test=test):
        ver, type, msg, _ = parse_msg(bits)
        result = sum_versions((ver, type, msg))
        print(line, '--', result)
    return result


async def part_2(test: bool = False) -> int:
    async for line, bits in get_binary_msg(test=test):
        ver, type, msg, _ = parse_msg(bits)
        result = sum_versions((ver, type, msg))
        print(line, '--', result)
    return result
