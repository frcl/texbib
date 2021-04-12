from .doi import from_doi
from .arxiv import from_arxiv
from .isbn import from_isbn
from .file import from_bibtex
from ..schemes import scheme_handler

from urllib.parse import urlparse


@scheme_handler('http', 'https')
def http_handler(uri):
    domain = urlparse(uri).netloc
    return {
        'arxiv.org': from_arxiv,
        'doi.org': from_doi,
    }[domain](uri)
