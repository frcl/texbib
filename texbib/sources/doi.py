import re
import requests
from ..schemes import scheme_handler


DOI = re.compile(r'(?:doi|DOI):([0-9.]*)/(.*)')
DOI_URL = re.compile(r'https?://doi.org/([0-9.]*)/([^/]*)')


@scheme_handler('doi', 'DOI')
def bibtex_from_doi(doi: str) -> str:
    """Get BibTeX for a DOI.

    Arguments:
        doi: Digital object identifier ("doi:10.xxxx/suffix")

    Returns:
        BibTeX string for the reference.
    """
    match = DOI.match(doi) or DOI_URL.match(doi)
    if not match:
        raise ValueError('Invalid DOI')

    crossref_url = (f'https://api.crossref.org/works/{match.group(1)}%2F'
                    f'{match.group(2)}/transform/application/x-bibtex')
    crossref_response = requests.get(crossref_url)
    crossref_response.raise_for_status()
    return crossref_response.text
