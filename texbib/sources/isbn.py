from typing import Tuple, Optional
from pathlib import Path
import isbnlib
import isbnlib.registry


to_bibtex = isbnlib.registry.bibformatters['bibtex']


def from_isbn(isbn: str) -> Tuple[Optional[str], Optional[Path]]:
    meta_info = isbnlib.meta(isbn)
    return to_bibtex(meta_info), None
