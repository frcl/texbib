import re
from pathlib import Path
import requests
from ..schemes import scheme_handler
from ..errors import BibError


ARXIV = re.compile(r'ar[xX]iv:(\d{4}\.\d*(?:v\d)?)')
ARXIV_OLDSTYLE = re.compile(r'ar[xX]iv:([a-zA-Z.]*/\d*)')


def _parse_arxiv_id(handle: str) -> str:
    match = ARXIV.match(handle)
    if not match:
        match = ARXIV_OLDSTYLE.match(handle)
        if not match:
            raise BibError('Invalid arXiv handle')
    return match.group(1)


@scheme_handler('arxiv', 'arXiv')
def bibtex_from_arxiv(handle: str) -> str:
    """Get BibTeX for an arXiv paper.

    Arguments:
        handle: ArXiv handle ("arXiv:jjmm.xxxxx")

    Returns:
        BibTeX string for the paper.
    """
    response = requests.get(f'https://arxiv.org/bibtex/{_parse_arxiv_id(handle)}')
    response.raise_for_status()
    return response.text


@scheme_handler('arxiv', 'arXiv', rtype='fulltext')
def fulltext_from_arxiv(handle: str, target: Path) -> Path:
    """Download PDF for an arXiv paper.

    Arguments:
        handle: ArXiv handle ("arXiv:jjmm.xxxxx")
        target: Path where the PDF should be saved.

    Returns:
        Path to the downloaded PDF file.
    """
    response = requests.get(f'https://arxiv.org/pdf/{_parse_arxiv_id(handle)}.pdf')
    response.raise_for_status()
    target.write_bytes(response.content)
    return target
