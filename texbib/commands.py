import os as _os

from .bibliography import Bibliography
from .exceptions import BibCodeError, BibKeyError


class CmdParser(object):

    def __init__(self, failfunc=lambda x: None, tellfunc=lambda x: None):
        self._fail = failfunc
        self._tell = tellfunc

    def add(self, *filenames):
        self.addto('all', *filenames)

    def rm(self, *identifyer):
        self.rmfrom('all', *identifyer)

    def dump(self, bibname='all', directory='.'):
        if not _os.path.exists(directory):
            self._fail("'{}' is not a directory".format(directory))
        with Bibliography(bibname) as bib:
            path = _os.path.join(directory, '{}.bib'.format(bibname))
            with open(path, 'w') as bibtexfile:
                bibtexfile.write(bib.bibtex())

    @staticmethod
    def show(bibname):
        with Bibliography(bibname) as bib:
            print(bib)

    @staticmethod
    def mkbib(bibname):
        with Bibliography(bibname, mode='n') as _:
            pass

    @staticmethod
    def rmbib(bibname):
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
                        self._tell(
                            "invalid Bibtex in file '{}'".format(filename))
                    except IOError:
                        self._tell(
                            "can not open file '{}'".format(filename))
                else:
                    self._tell(
                        "file '{}' not in directory".format(filename))

    def rmfrom(self, bibname, *identifyers):
        with Bibliography(bibname) as bib:
            for identifyer in list(identifyers):
                try:
                    del bib[identifyer]
                except BibKeyError:
                    self._fail("No item with ID '{}' in {}".format(
                        identifyer, bibname))

    @staticmethod
    def searchin(bibname, pattern):
        with Bibliography(bibname) as bib:
            print('\n'.join(map(str, bib.search(pattern))))

    @staticmethod
    def cleanup(bibname='all'):
        with Bibliography(bibname) as bib:
            bib.cleanup()

    def chid(self, identifyer, new_identifyer):
        pass

    def chcont(self, identifyer, attribute, value):
        pass

