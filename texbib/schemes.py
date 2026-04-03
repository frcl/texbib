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
