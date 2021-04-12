from ..schemes import file_handler


@file_handler('.bib', '.bibtex')
def from_bibtex(path):
    with path.open() as infile:
        bibtex = infile.read()
    return bibtex, None
