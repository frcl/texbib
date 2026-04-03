from urllib.parse import urlparse
from .doi import bibtex_from_doi
from .arxiv import bibtex_from_arxiv, fulltext_from_arxiv
from .isbn import bibtex_from_isbn
from .file import bibtex_from_file
from ..errors import UnkownResource
from ..schemes import scheme_handler


DOMAIN_HANDLERS = {
    'arxiv.org': bibtex_from_arxiv,
    'doi.org': bibtex_from_doi,
}


@scheme_handler('http', 'https')
def http_handler(uri):
    domain = urlparse(uri).netloc
    try:
        return DOMAIN_HANDLERS[domain](uri)
    except KeyError as exc:
        raise UnkownResource(uri) from exc
