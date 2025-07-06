from __future__ import annotations

import argparse
import os
from . import DocGenerator, walk_python_files


parser = argparse.ArgumentParser(__package__)
parser.add_argument("dir_or_file", nargs=1)

if __name__ == "__main__":
    args = parser.parse_args()
    dir_or_file: str = args.dir_or_file[0]
    if os.path.isdir(dir_or_file):
        files = walk_python_files(dir_or_file)
    else:
        files = [dir_or_file]

    docgen = DocGenerator()
    for file in files:
        with open(file, "r") as f:
            code = f.read()
            docgen.parse_code(code)
    print(docgen.output())
