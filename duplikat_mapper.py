import os
import better_exceptions
from pathlib import Path
import hashlib
from collections import defaultdict
import json

mapper = defaultdict(list)

def function_over_files(path):
    for fname in path.iterdir():
        if fname.is_dir():
            function_over_files(fname)

    mapper[md5_dir(path)].append(path)
    print(path)

def md5_update_from_dir(directory, hash):
    assert directory.is_dir()
    for path in Path(directory).iterdir():
        # hash.update(path.name.encode())
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash.update(chunk)
            # print(path, end='\r')
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
            # mapper[hash.hexdigest()].append(path)
            print(path, end='\r')
    return hash


def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()

if __name__ == '__main__':
    # src = Path("/mnt/o/arkiver/")
    b = Path('/mnt/o/arkiver/')
    # c =list(b.glob('**/'))
    # g = list(set(c) ^set([i.parent for i in c]) )
    # g.remove(b.parent)
    
    for a in b.glob('**/'):
        if a in [b, b.joinpath("Kristina"), b.joinpath("Macbook før mai2018"), b.joinpath("ola imac")]:
            print("Hoppa over ", a)|1
            continue
        print(a)
        mapper[md5_dir(a)].append(a)

    with open(Path('duplikatar.json'), 'w', encoding='utf-8') as f:
        json.dump(mapper, f, indent=4, ensure_ascii=False, sort_keys=True)

    for md5,path in mapper.items():
        if len(path)> 1:
            print(path)
