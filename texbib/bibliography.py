import os as _os
import re as _re
import json as _json
import dbm.gnu as _gdbm

try:
    from bibtexparser import loads as _loads
    from bibtexparser import dumps as _dumps
    from bibtexparser.bibdatabase import BibDatabase as _BibDatabase
except ImportError:
    import importlib.util
    _spec = importlib.util.spec_from_file_location(
        'bibtexparser',
        _os.path.join(_os.environ['BIBTEXPARSERDIR'], '__init__.py'))
    _btparser = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_btparser)
    _loads = _btparser.loads
    _dumps = _btparser.dumps
    _BibDatabase = _btparser.bibdatabase.BibDatabase

from .colors import ColoredText as _ct


class BibNameError(NameError):
    pass

class BibKeyError(KeyError):
    pass

class BibCodeError(Exception):
    pass

class DatabaseError(Exception):
    pass


class Bibliography(object):
    """A class to manage bibliographic data in a database.
    It mimics a dictionary with bibtex ids as keys and
    returns a BibItem, wich is also dinctionary like.
    It can be seen as a wrapper around dbm.gnu.
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
        self.close()

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

    def close(self):
        self.gdb.close()

    @property
    def path(self):
        return self._path.format(self.name)

    def update(self, bibcode):
        try:
            entries = _loads(bibcode).get_entry_dict()
        except Exception:
            raise BibCodeError

        for key in entries.keys():
            self[key] = BibItem(entries[key])

    def ids(self):
        return self.gdb.keys()

    def values(self):
        return [self[k] for k in self.ids()]

    def bibtex(self):
        bib_db = _BibDatabase()
        bib_db.entries = self.values()
        return _dumps(bib_db)

    def search(self, pattern):
        for i in self.ids():
            if _re.match(pattern, i.decode('utf-8')):
                yield self[i]

    def cleanup(self, mode=None):
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

