from pathlib import Path


def rm_tree(path: Path):
    path = Path(path)
    for child in path.iterdir():
        if child.is_dir():
            rm_tree(child)
        else:
            child.unlink()
    path.rmdir()
