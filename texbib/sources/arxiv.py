import re
from typing import Tuple, Optional
from pathlib import Path
import requests
from ..schemes import scheme_handler


ARXIV = re.compile(r'ar[xX]iv:(\d{4}\.\d*(?:v\d)?)')
ARXIV_OLDSTYLE = re.compile(r'ar[xX]iv:([a-zA-Z.]*/\d*)')


@scheme_handler('arxiv', 'arXiv')
def from_arxiv(handle: str) -> Tuple[Optional[str], Optional[Path]]:
    """Get a paper from arXiv.

    Arguments:
        handle (str): ArXiv handle ("arXiv:jjmm.xxxxx")

    Returns:
        bibtex (str): the bibtex code for the reference
        pdf_path (pathlib.Path): a Path to the downloaded PDF
    """
    match = ARXIV.match(handle)
    if not match:
        match = ARXIV_OLDSTYLE.match(handle)
        if not match:
            raise ValueError('Invalid arXiv handle')

    bibtex_url = f'https://arxiv.org/bibtex/{match.group(1)}'
    arxiv_response = requests.get(bibtex_url)
    arxiv_response.raise_for_status()
    bibtex = arxiv_response.text

    # pdf_url = f'https://arxiv.org/pdf/{match.group(1)}'
    # TODO: download pdf

    return bibtex, None
