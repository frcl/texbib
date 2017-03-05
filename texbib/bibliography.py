import re
import shelve
from pathlib import Path as Path
from typing import Union

from texbib.parser import loads, dumps
from texbib.colors import ColoredText as _ct


class BibItem(dict):
    """A dictionary like class that contains data about a single reference.
    A bibitem should always have an ID, author, year and title.
    There can be an arbitrary number other entries.
    """

    def __init__(self, item):
        dict.__init__(self)

        if isinstance(item, dict):
            self.update(item)
        else:
            raise TypeError

    def __str__(self):
        info = [str(_ct(self['ID'], 'ID')),
                '{} ({})'.format(self['author'],
                                 self['year']),
                self['title']]
        return '\n\t'.join(info)


class Bibliography(object):
    """A class to manage bibliographic data in a database.
    It mimics a dictionary with bibtex ids as keys and
    returns a BibItem, wich is also dinctionary-like.
    Technically it is a wrapper around the dbm.gnu database.
    """

    def __init__(self, path: Union[Path, str], mode: str = 'r') -> None:
        self.mode = mode

        self.path = Path(path)

        self.db = shelve.open(str(self.path), mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def __getitem__(self, key: str):
        return BibItem(self.db[key])

    def __setitem__(self, key: str, bibitem: BibItem):
        self.db[key] = bibitem

    def __contains__(self, identifyer: str):
        return identifyer in self.ids()

    def __len__(self):
        return len(self.db)

    def __iter__(self):
        return self.ids()

    def __str__(self):
        return '\n'.join(str(self[key]) for key in self)

    def update(self, data):
        """Simular to dict.update. Data can be
        either a Bibliogrphy or a BibTex string."""
        if isinstance(data, str):
            entries = loads(data)
            for key in entries:
                self[key] = BibItem(entries[key])
        elif isinstance(data, Bibliography):
            for key in data.ids():
                self[key] = data[key]
        else:
            raise TypeError('Can not read {}'.format(type(data)))

    def remove(self, key: str):
        del self.db[key]

    def ids(self):
        """IDs in the bibliography. Simular to dict.keys."""
        for key in self.db.keys():
            yield key

    def values(self):
        """Simular to dict.values.
        Returns list of BibItems."""
        for val in self.db.values():
            yield val

    def items(self):
        """Simular to dict.items.
        Returns list of (ID, BibItem) tuples."""
        for key, val in self.db.items():
            yield key, val

    def bibtex(self):
        """Returns a single string with the bibtex
        code of all items in the bibliography"""
        return dumps(self)

    def search(self, pattern):
        """Find all matches of the pattern in the bibliography.
        Only goes through IDs at the moment."""
        for key in self.ids():
            if re.match(pattern, key):
                yield self[key]

    def cleanup(self):
        """Try to reduce memory usage, by reorganizing
        database and deleting unnessecary fields"""
        pass # TODO: implement

    def close(self):
        self.db.close()
