import os, re, json
import dbm.gnu as gdbm

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


class DatabaseError(NameError):
    pass

class BibNameError(NameError):
    pass

class BibCodeError(Exception):
    pass

class Bibliography(object):

    def __init__(self, bibname=None):
        self.name = bibname
        try:
            self.texbibdir = os.environ['TEXBIBDIR']
        except KeyError:
            self.texbibdir = os.path.join(os.environ['HOME'],'.texbib' )
        self._path = os.path.join(self.texbibdir,'{}.gdbm')
        if not bibname:
            return

        try:
            self.db = gdbm.open(self.path,'c')
        except:
            raise DatabaseError

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #self.db.sync()
        self.db.close()
    
    @property
    def path(self):
        return self._path.format(self.name)

    def merge_from_file(self, filename):
        try:
            with open(filename) as f:
                entries = bibtexparser.load(f).get_entry_dict()
        except:
            raise BibCodeError

        for key in entries.keys():
            self.db[key] = json.dumps(entries[key])

    def dump(self, path):
        bib_db = BibDatabase()
        bib_db.entries = [json.loads(self.db[k].decode('utf-8')) for k in self.db.keys()]

        with open(path,'w') as f:
            bibtexparser.dump(bib_db,f)

    def reorganize(self):
        self.db.reorganize()

    def merge(self, bib):
        self.db.update(bib)

    def del_item(self, identifier):
        del self.db[identifier]

