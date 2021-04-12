SCHEMES = {}
EXTENSIONS = {}


def scheme_handler(*schemes):
    def decorator(handler):
        for scheme in schemes:
            SCHEMES[scheme] = handler
        return handler
    return decorator


def file_handler(*extensions):
    def decorator(handler):
        for ext in extensions:
            EXTENSIONS[ext] = handler
        return handler
    return decorator
