import re
from typing import Tuple, Optional
from pathlib import Path
import bs4
import requests


DOI = re.compile(r'doi:([0-9.]*)/(.*)')
DOI_URL = re.compile(r'https?://doi.org/([0-9.]*)/([^/]*)')


def from_doi(doi: str) -> Tuple[Optional[str], Optional[Path]]:
    """Get resource from DOI.

    Arguments:
        doi (str): Digital object identifier ("doi:10.xxxx/suffix")

    Returns:
        bibtex (str): the bibtex code for the reference
        pdf_path (pathlib.Path): a Path to the downloaded PDF
    """
    match = DOI.match(doi) or DOI_URL.match(doi)
    if not match:
        raise ValueError('Invalid DOI')

    url = f'https://doi.org/{match.group(1)}%2F{match.group(2)}'
    # response = requests.get(url)
    # soup = bs4.BeautifulSoup(response.text)
    # pdf_urls = soup.find_all('a', {'href': re.compile('.*\.pdf')})
    # if pdf_urls:
        #TODO

    # alternative: sci-hub

    crossref_url = (f'https://api.crossref.org/works/{match.group(1)}%2F'
                    f'{match.group(2)}/transform/application/x-bibtex')
    crossref_response = requests.get(crossref_url)
    crossref_response.raise_for_status()
    bibtex = crossref_response.text
    return bibtex, None
