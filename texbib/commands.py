import os as _os
from .bibliography import Bibliography
from .exceptions import BibCodeError, BibKeyError

class CmdParser:

    def __init__(self, failfunc=lambda x: None, tellfunc=lambda x: None):
        self.fail = failfunc
        self.tell = tellfunc

    def add(self, *filenames):
        self.addto('all', *filenames)

    def rm(self, *identifyer):
        self.rmfrom('all', *identifyer)

    def dump(self, bibname='all', directory='.'):
        if not _os.path.exists(directory):
            self.fail("'{}' is not a directory".format(directory))
        with Bibliography(bibname) as bib:
            path = _os.path.join(directory, '{}.bib'.format(bibname))
            with open(path, 'w') as bibtexfile:
                bibtexfile.write(bib.bibtex())

    def show(self, bibname):
        with Bibliography(bibname) as bib:
            print(bib)

    def mkbib(self, bibname):
        with Bibliography(bibname, mode='m') as _:
            pass

    def rmbib(self, bibname):
        with Bibliography(bibname) as bib:
            _os.remove(bib.path)

    def addto(self, bibname, *filenames):
        with Bibliography(bibname) as bib:
            for filename in list(filenames):
                if _os.path.exists(filename):
                    try:
                        with open(filename, 'r') as bibtexfile:
                            bib.update(bibtexfile.read())
                    except BibCodeError:
                        self.tell(
                            "invalid Bibtex in file '{}'".format(filename))
                    except IOError:
                        self.tell(
                            "can not open file '{}'".format(filename))
                else:
                    self.tell(
                        "file '{}' not in directory".format(filename))

    def rmfrom(self, bibname, *identifyers):
        with Bibliography(bibname) as bib:
            for identifyer in list(identifyers):
                try:
                    del bib[identifyer]
                except BibKeyError:
                    self.fail("No item with ID '{}' in {}".format(
                        identifyer, bibname))

    def searchin(self, bibname, pattern):
        with Bibliography(bibname) as bib:
            print('\n'.join(map(str, bib.search(pattern))))

    def cleanup(self, bibname='all'):
        with Bibliography(bibname) as bib:
            bib.cleanup()

    def chid(self, identifyer, new_identifyer):
        pass

    def chcont(self, identifyer, attribute, value):
        pass

