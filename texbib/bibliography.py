import os as _os
import re as _re
import json as _json
import dbm.gnu as _gdbm

try:
    from bibtexparser import loads as _loads
    from bibtexparser import dumps as _dumps
    from bibtexparser.bibdatabase import BibDatabase as _BibDatabase
except ImportError:
    from importutil.importBibtexParser import import_from_dir
    _loads, _dumps, _BibDatabase = \
            import_from_dir(_os.environ['BIBTEXPARSERDIR'])

from .colors import ColoredText as _ct
from .exceptions import *



class Bibliography(object):
    """A class to manage bibliographic data in a database.
    It mimics a dictionary with bibtex ids as keys and
    returns a BibItem, wich is also dinctionary-like.
    Technically it is a wrapper around the dbm.gnu database.
    """

    def __init__(self, bibname=None, mode='o'):
        self.name = bibname

        try:
            self.texbibdir = _os.environ['TEXBIBDIR']
        except KeyError:
            self.texbibdir = _os.path.join(
                _os.environ['HOME'], '.texbib')
        self._path = _os.path.join(self.texbibdir, '{}.gdbm')

        if not bibname:
            return
        if not _os.path.exists(self._path.format(bibname)):
            if mode is 'm':
                pass
            elif mode is 'o':
                raise BibNameError

        try:
            self.gdb = _gdbm.open(self.path, 'c')
        except Exception:
            raise DatabaseError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.gdb.close()

    def __getitem__(self, key):
        try:
            return BibItem(self.gdb[key])
        except KeyError:
            raise BibKeyError
        except Exception:
            raise DatabaseError

    def __setitem__(self, key, bibitem):
        self.gdb[key] = repr(bibitem)

    def __delitem__(self, key):
        del self.gdb[key]

    def __contains__(self, identifyer):
        return identifyer in self.ids()

    def __len__(self):
        return len(self.ids())

    def __iter__(self):
        return iter(self.ids())

    def __str__(self):
        return '\n'.join([str(self[key]) for key in self])

    @property
    def path(self):
        """Path to the gdbm file of the bibliography"""
        return self._path.format(self.name)

    def update(self, bibcode):
        """Simular to dict.update."""
        try:
            entries = _loads(bibcode).get_entry_dict()
        except Exception:
            raise BibCodeError

        for key in entries.keys():
            self[key] = BibItem(entries[key])

    def ids(self):
        """IDs in the bibliography. Simular to dict.keys."""
        return self.gdb.keys()

    def values(self):
        """Simular to dict.values.
        Returns list of BibItems."""
        return [self[k] for k in self.ids()]

    def bibtex(self):
        """Returns a single string with the bibtex
        code of all items in the bibliography"""
        bib_db = _BibDatabase()
        bib_db.entries = self.values()
        return _dumps(bib_db)

    def search(self, pattern):
        """Find all matches of the pattern in the bibliography.
        Only goes through IDs at the moment."""
        for i in self.ids():
            if _re.match(pattern, i.decode('utf-8')):
                yield self[i]

    def cleanup(self, mode=None):
        """Try to reduce memory usage, by reorganizing
        database and deleting unnessecary fields"""
        if mode is 'scopus':
            pass #TODO: implement deletion of scopus tags
            #for key in self.db.keys():
            #    self.db[key] = BibItem
        self.gdb.reorganize()

class BibItem(dict):
    """A dictionary like class that contains data about a single reference.
    A bibitem should always have an ID, author, year and title.
    There can be an arbitrary number other entries.
    """

    def __init__(self, item):
        dict.__init__(self)
        if isinstance(item, dict):
            self.update(item)
        elif isinstance(item, bytes):
            self.update(_json.loads(item.decode('utf-8')))

    def __str__(self):
        info = [str(_ct(self['ID'], 'ID')),
                '{} ({})'.format(self['author'],
                                 self['year']),
                self['title']]
        return '\n    '.join(info)

    def __repr__(self):
        return _json.dumps(self)

