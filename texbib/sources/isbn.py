import warnings
from typing import Tuple, Optional
from pathlib import Path

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import isbnlib
    to_bibtex = lambda x: isbnlib.dev._fmt._fmtbib('bibtex', x)


from ..schemes import scheme_handler


@scheme_handler('isbn', 'ISBN')
def from_isbn(isbn: str) -> Tuple[Optional[str], Optional[Path]]:
    meta_info = isbnlib.meta(isbn)
    return to_bibtex(meta_info), None
