from typing import Optional


SCHEMES = {'bibtex': {}, 'fulltext': {}}
EXTENSIONS = {}


def scheme_handler(*schemes, rtype='bibtex'):
    def decorator(handler):
        SCHEMES[rtype][schemes[0]] = handler
        for scheme in schemes:
            SCHEMES[rtype][scheme] = handler
        return handler
    return decorator


def file_handler(*extensions):
    def decorator(handler):
        for ext in extensions:
            EXTENSIONS[ext] = handler
        return handler
    return decorator


def get_scheme(obj: str) -> Optional[str]:
    """Extract the scheme prefix from an object string.

    Returns:
        Scheme name (e.g., 'doi', 'arxiv', 'isbn') or None if no scheme.
    """
    if ':' in obj:
        scheme = obj.split(':', 1)[0]
        if scheme in SCHEMES['bibtex']:
            return scheme
    return None
