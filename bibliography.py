import os, re, json
import dbm.gnu as gdbm
try:
    from bibtexparser import loads, dumps
    from bibtexparser.bibdatabase import BibDatabase
except ImportError:
    execfile(os.path.join(os.environ['BIBTEXPARSERDIR'], '__init__.py'))
    BibDatabase = bibdatabase.BibDatabase

class BibNameError(NameError):
    pass

class BibKeyError(KeyError):
    pass

class BibCodeError(Exception):
    pass

class DatabaseError(Exception):
    pass

class Bibliography(object):

    def __init__(self, bibname=None, mode='o'):
        self.name = bibname
        try:
            self.texbibdir = os.environ['TEXBIBDIR']
        except KeyError:
            self.texbibdir = os.path.join(
                    os.environ['HOME'],'.texbib' )
        self._path = os.path.join(self.texbibdir,'{}.gdbm')
        if not bibname:
            return
        if not os.path.exists(self._path.format(bibname)):
            if mode is 'm':
                pass
            elif mode is 'o':
                raise BibNameError

        try:
            self.db = gdbm.open(self.path,'c')
        except Exception:
            raise DatabaseError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def __getitem__(self, key):
        try:
            return BibItem(self.db[key])
        except KeyError:
            raise BibKeyError
        except Exception:
            raise DatabaseError

    def __setitem__(self, key, bibitem):
        self.db[key] = repr(bibitem)

    def __delitem__(self, key):
        del self.db[key]

    def __contains__(self, identifyer):
        return identifyer in self.db.keys()

    def __len__(self):
        return len(self.ids())

    def __iter__(self):
        return iter(self.ids())
    
    def __str__(self):
        return '\n'.join([str(self[key]) for key in self])

    def close(self):
        self.db.close()

    @property
    def path(self):
        return self._path.format(self.name)

    def update(self, bibcode):
        try:
            entries = loads(bibcode).get_entry_dict()
        except Exception:
            raise BibCodeError

        for key in entries.keys():
            self[key] = BibItem(entries[key])

    def ids(self):
        return self.db.keys()

    def values(self):
        return [self[k] for k in self.ids()]

    def bibtex(self):
        bib_db = BibDatabase()
        bib_db.entries = self.values()
        return dumps(bib_db)

    def cleanup(self, mode=None):
        if mode is 'scopus':
            pass
            #for key in self.db.keys():
            #    self.db[key] = BibItem
        self.db.reorganize()

class BibItem(dict):
    def __init__(self, itembytes):
        try:
            self.update(itembytes)
        except:
            self.update(json.loads(itembytes.decode('utf-8')))

    def __str__(self):
        info = [self['ID'],
                '{}, {}'.format(self['author'],
                self['year']),
                self['title']]
        return '\n    '.join(info)

    def __repr__(self):
        return json.dumps(self)

