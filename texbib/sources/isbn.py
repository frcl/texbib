import warnings
from pathlib import Path

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import isbnlib

from ..schemes import scheme_handler


def _to_bibtex(meta):
    return isbnlib.dev._fmt._fmtbib('bibtex', meta)


@scheme_handler('isbn', 'ISBN')
def bibtex_from_isbn(isbn: str) -> str:
    """Get BibTeX for an ISBN.

    Arguments:
        isbn: International Standard Book Number

    Returns:
        BibTeX string for the book.
    """
    return _to_bibtex(isbnlib.meta(isbn))
