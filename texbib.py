import os
import argparse

from bibliography import *

def _main():
    args = argparse.ArgumentParser()

    args.add_argument('command')
    args.add_argument('args', nargs='*')

    args = args.parse_args()

    cmd = args.command
    cmd_args = args.args
    cmd_parser = _CmdParser()

    if hasattr(cmd_parser, cmd):
        cmd_func = getattr(cmd_parser, cmd)
        try:
            cmd_func(*cmd_args)
        except TypeError:
            _fail('wrong number of arguments')
        except BibNameError:
            _fail('unknown bibname')
        except DatabaseError:
            _fail('database currupt')
    else:
        _fail('unknown command')

def _tell(msg):
    print('texbib: {}'.format(msg))

def _fail(msg):
    print('texbib: {}'.format(msg))
    quit()

class _CmdParser(object):
    def add(self, *filenames):
        self.addto('all', *filenames)

    def rm(self, *identifyer):
        self.rmfrom('all', *identifyer)

    def dump(self, bibname='all', directory='.'):
        if not os.path.exists(directory):
            _fail("'{}' is not a directory".format(directory))
        with Bibliography(bibname) as bib:
            path = os.path.join(
                    directory,'{}.bib'.format(bibname))
            with open(path,'w') as f:
                f.write(bib.bibtex())

    def show(self, bibname):
        with Bibliography(bibname) as bib:
            print(bib)

    def mkbib(self, bibname):
        with Bibliography(bibname,mode='m') as bib:
            pass

    def rmbib(self, bibname):
        with Bibliography(bibname) as bib:
            os.remove(bib.path)

    def addto(self, bibname, *filenames):
        with Bibliography(bibname) as bib:
            for fn in list(filenames):
                if os.path.exists(fn):
                    try:
                        with open(fn,'r') as f:
                            bib.update(f.read())
                    except BibCodeError:
                        _tell(
                        "invalid Bibtex in file '{}'".format(fn))
#                    except Exception:
#                        _tell(
#                        "can not open file '{}'".format(fn))
                else:
                    _tell(
                    "file '{}' not in directory".format(fn))

    def rmfrom(self, bibname, *identifyer):
        with Bibliography(bibname) as bib:
            for Id in list(identifyer):
                try:
                    del bib[Id]
                except BibKeyError:
                    _fail(
                    "No item with ID '{}' in {}".format(
                            Id,bibname))

    def cleanup(self, bibname='all'):
        with Bibliography(bibname) as bib:
            bib.cleanup()

    def chid(self, identifyer, new_identifyer):
        pass

    def chcont(self, identifyer, attribute, value):
        pass

if __name__ == '__main__':
    _main()

