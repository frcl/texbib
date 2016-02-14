"""Exceptions raised by texbib in case
of bibtex or database related errors"""

class BibNameError(NameError):
    pass

class BibKeyError(KeyError):
    pass

class BibCodeError(Exception):
    pass

class DatabaseError(Exception):
    pass

