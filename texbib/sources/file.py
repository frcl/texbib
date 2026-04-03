import chardet
from pathlib import Path
from ..schemes import file_handler


@file_handler('.bib', '.bibtex')
def bibtex_from_file(path: Path) -> str:
    """Read BibTeX from a file with automatic encoding detection.

    Arguments:
        path: Path to the .bib or .bibtex file.

    Returns:
        BibTeX string with UTF-8 encoding.
    """
    raw = path.read_bytes()
    detected = chardet.detect(raw)
    return raw.decode(detected['encoding'] or 'utf-8')
