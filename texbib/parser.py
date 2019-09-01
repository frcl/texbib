from bibtexparser import loads as _loads
from bibtexparser import dumps as _dumps
from bibtexparser.bibdatabase import BibDatabase as _BibDatabase


def loads(bibtexcode):
    """Reads a string with bibtex data and returns a dictionary of
    the references with IDs as Keys. If a reference contains no ID,
    one is generated from the data. Raises if bibtexcode is not valid."""
    if not bibtexcode:
        return {}
    else:
        return _loads(bibtexcode).get_entry_dict()

def dumps(bib):
    """Read a dict shaped like one created by `loads`
    (or a `texbib.Bibliogrphy` object) and returns a
    string containing bibtex references."""
    bib_db = _BibDatabase()
    bib_db.entries = bib.values()
    return _dumps(bib_db)
