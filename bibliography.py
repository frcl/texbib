import os, re, json

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


class DatabaseError(NameError):
    pass

class BibNameError(NameError):
    pass

class BibCodeError(Exception):
    pass

class Bibliography(dict):

    def __init__(self, bibname=None):
        self.name = bibname
        try:
            self.texbibdir = os.environ['TEXBIBDIR']
        except:
            self.texbibdir = os.path.join(os.environ['HOME'],'.texbib' )
        self._path = os.path.join(self.texbibdir,'{}.json')
        if not bibname:
            return

        if not os.path.exists(self.path):
            raise BibNameError
        try:
            with open(self.path, 'r') as f:
                self.update(json.load(f))
        except:
            raise DatabaseError
    
    @property
    def path(self):
        return self._path.format(self.name)

    def merge_from_file(self, filename):
        try:
            with open(filename) as f:
                self.update(bibtexparser.load(f).get_entry_dict())
        except:
            raise BibCodeError

    def dump(self, path):
        bib_db = BibDatabase()
        bib_db.entries = list(self.values())
        
        with open(path,'w') as f:
            bibtexparser.dump(bib_db,f)

    def merge(self, bib):
        self.extend(bib)

    def store(self):
        if not self.name:
            raise BibNameError
        with open(self.path,'w') as f:
            f.write(json.dumps(self))

