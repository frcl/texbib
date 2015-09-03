import os
import argparse

from bibliography import *

class CmdParser(object):
    def add(self, *filenames):
        self.addto('all', *filenames)

    def rm(self, identifyer):
        pass

    def dump(self, bibname='all', directory='.'):
        if not os.path.exists(directory):
            fail("'{}' is not a directory".format(directory))

    def mkbib(self, bibname):
        bib = Bibliography()
        bib.name = bibname
        if os.path.exists(bib.path):
            fail("bib '{}' already exists".format(bibname))
        bib.store()

    def rmbib(self, bibname):
        bib = Bibliography()
        bib.name = bibname
        if not os.path.exists(bib.path):
            fail("bib '{}' already exists".format(bibname))
        os.remove(bib.path)

    def addto(self, bibname, *filenames):
        try:
            bib = Bibliography(bibname)
        except BibNameError:
            fail("bib '{}' does not exist".format(bibname))

        for fn in list(filenames):
            if not os.path.exists(fn):
                tell("file '{}' not in directory".format(fn))
            else:
                try:
                    bib.merge_from_file(fn)
                except BibCodeError:
                    tell("invalid Bibtex Code \
                            in file '{}'".format(filename))
        bib.store(bibname)

    def rmfrom(self, bibname, identifyer):
        pass

    def chid(self, identifyer, new_identifyer):
        pass

    def chcont(self, identifyer, attribute, value):
        pass

def main():
    args = argparse.ArgumentParser()

    args.add_argument('command')
    args.add_argument('args', nargs='*')

    args = args.parse_args()

    cmd = args.command
    cmd_args = args.args
    cmd_parser = CmdParser()

    if hasattr(cmd_parser, cmd):
        cmd_func = getattr(cmd_parser, cmd)
        try:
            cmd_func(*cmd_args)
        except TypeError:
            fail('wrong number of arguments')
    else:
        fail('unknown command')


def tell(msg):
    print('texbib: {}'.format(msg))

def fail(msg):
    print('texbib: {}'.format(msg))
    quit()

if __name__ == '__main__':
    main()

    #add	add a BibTex content from FILE to your libary
    #rm	        remove the item ID from your libary
    #dump	create a Bibtex file from BIB in the current directory
    #mkbib	create a bibligraphy named NAME
    #rmbib	remove the bibligraphy named BIB
    #addto	add BibTex content from FILE or item ID to your bibliogrphy named BIB
    #rmfrom	remove BibTex item ID from your bibliogrphy named BIB
    #chid	change the identifyer of ID to NEW
    #chcont	change the attribute ATTR of ID to NEW
