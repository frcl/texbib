import re
import shelve
from pathlib import Path as Path
from typing import Union

from texbib.parser import loads, dumps
from texbib.colors import ColoredText as _ct


class Bibliography(object):
    """A class to manage bibliographic data in a database.
    It mimics a dictionary with bibtex ids as keys and
    returns a BibItem, wich is also dinctionary-like.
    Technically it is a wrapper around the dbm.gnu database.
    """

    def __init__(self, path: Union[Path, str], mode: str = 'o'):
        self.mode = mode

        self.path = Path(path)

        if self.path.exists():
            self.db = shelve.open(str(self.path), 'w')
        else:
            if mode == 'n':
                self.db = shelve.open(str(self.path), 'c')
            elif mode == 'e':
                pass
            elif mode == 'o':
                raise IOError('{} not found'.format(path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def __getitem__(self, key):
        return BibItem(self.db[key])

    def __setitem__(self, key, bibitem):
        self.db[key] = bibitem

    def __contains__(self, identifyer):
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

    def remove(self, key):
        del self.db[key]

    def ids(self):
        """IDs in the bibliography. Simular to dict.keys."""
        for key in self.db.keys():
            yield key

    def values(self):
        """Simular to dict.values.
        Returns list of BibItems."""
        for key in self.ids():
            yield self[key]

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

    def cleanup(self, mode=None):
        """Try to reduce memory usage, by reorganizing
        database and deleting unnessecary fields"""
        if mode == 'scopus':
            pass #TODO: implement deletion of scopus tags
            #for key in self.db.keys():
            #    self.db[key] = BibItem

    def close(self):
        self.db.close()


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
