from pathlib import Path
from enum import Enum


class Events(Enum):
    FileNotFound = 1
    IdNotFound = 2
    NoEffect = 3
    InvalidName = 4
    FailedAccess = 5

    def __str__(self):
        return '{event}'.format(event=self.name)


class Levels(Enum):
    info = 1
    warning = 2
    error = 3
    critical = 4

    def __str__(self):
        return '{level}'\
               .format(level=self.name.upper()) # pylint: disable=no-member


def rm_tree(path: Path):
    path = Path(path)
    for child in path.iterdir():
        if child.is_dir():
            rm_tree(child)
        else:
            child.unlink()
    path.rmdir()
