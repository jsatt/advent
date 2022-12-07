from typing import Generator, Iterable, Iterator, Mapping, Optional, Union

def read_file(test: bool = False) -> Generator[str, None, None]:
    if test:
        file_name = 'test_input.txt'
    else:
        file_name = 'input.txt'

    with open(file_name, 'r', encoding='utf8') as f:
        for line in f.readlines():
            yield line.strip()


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def __repr__(self) -> str:
        return f'{self.name} (file, size={self.size})'

    def get_size(self) -> int:
        return self.size


class Dir:
    def __init__(self, name: str, parent: Optional['Dir']):
        self.name = name
        self.parent = parent
        self.contents = {}

    def __repr__(self) -> str:
        return (
            f'{self.name} (dir, size={self.size})\n'
            '\n'.join([f'{repr(c)}' for _, c in self.contents.items()])
        )

    def __iter__(self) -> Generator[Union[File, 'Dir'], None, None]:
        yield from self.contents.values()

    @property
    def size(self) -> int:
        return sum([c.size for _, c in self.contents.items()])

    def add_child(self, name: str, size: Optional[int]) -> Union[File, 'Dir']:
        if size is None:
            content = Dir(name, self)
        else:
            content = File(name, size)
        self.contents[name] = content
        return content

def build_fs(lines: Iterator[str]) -> Dir:
    line = next(lines)
    fs = Dir('/', None)
    current_dir = fs
    for line in lines:
        parts = line.split(' ')
        if parts[0] == '$':
            if parts[1] == 'cd':
                if parts[2] == '/':
                    current_dir = fs
                elif parts[2] == '..' and current_dir.parent:
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir.contents[parts[2]]
            elif parts[1] == 'ls':
                pass
        elif parts[0] == 'dir':
            current_dir.add_child(parts[1], None)
        else:
            current_dir.add_child(parts[1], int(parts[0]))
    return fs

def traverse_fs(fs: Dir, min_size: int, max_size: int) -> Iterable[int]:
    sub_100k = []
    for obj in fs:
        if isinstance(obj, Dir):
            if min_size < obj.size <= max_size:
                sub_100k.append(obj.size)
            sub_100k.extend(traverse_fs(obj, min_size, max_size))
    return sub_100k

def part_1(test: bool = False) -> int:
    lines = read_file(test)
    fs = build_fs(lines)
    sub_100k = traverse_fs(fs, 0, 100_000)
    return sum(sub_100k)

def part_2(test: bool = False) -> int:
    lines = read_file(test)
    fs = build_fs(lines)
    unused = 70_000_000 - fs.size
    required = 30_000_000
    target_size = required - unused
    sub_100k = traverse_fs(fs, target_size, required)
    return min(sub_100k)
