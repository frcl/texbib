import chardet

from ..schemes import file_handler


@file_handler('.bib', '.bibtex')
def from_bibtex(path):
    raw = path.read_bytes()
    detected = chardet.detect(raw)
    source_encoding = detected['encoding'] or 'utf-8'
    bibtex = raw.decode(source_encoding)
    return bibtex, None
