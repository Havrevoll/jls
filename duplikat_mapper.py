import os
import better_exceptions
from pathlib import Path
import hashlib
from collections import defaultdict

mapper = defaultdict(list)

def function_over_files(path):
    for fname in path.iterdir():
        if fname.is_dir():
            function_over_files(fname)

    mapper[md5_dir(path)].append(path)
    print(path)

def md5_update_from_dir(directory, hash):
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash.update(chunk)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
            mapper[hash].append(path)
            print(path)
    return hash


def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()

if __name__ == '__main__':
    src = Path("/mnt/o/arkiver/")
    mapper = md5_dir(src)

    for md5,path in mapper.items():
        if len(path)> 1:
            print(path)
