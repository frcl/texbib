import os as _os

from texbib.bibliography import Bibliography
from texbib.utils import runtime_action, CmdTracker


commands = CmdTracker()


@commands.register
def add(filenames):
    # TODO: get active bibname
    bibname = 'all'
    with Bibliography(bibname) as bib:
        for filename in list(filenames):
            if _os.path.exists(filename):
                try:
                    with open(filename) as bibtexfile:
                        bib.update(bibtexfile.read())
                except ValueError:
                    runtime_action(
                        "invalid Bibtex in file '{}'".format(filename))
                except IOError:
                    runtime_action(
                        "can not open file '{}'".format(filename))
            else:
                runtime_action(
                    "file '{}' not in directory".format(filename))

@commands.register
def rm(identifyers):
    # TODO: get active bibname
    bibname = 'all'
    with Bibliography(bibname) as bib:
        for identifyer in list(identifyers):
            try:
                bib.remove(identifyer)
            except KeyError:
                runtime_action("No item with ID '{}' in {}"
                               .format(identifyer, bibname),
                               action='fail')
                # TODO: tell or check befor removing


@commands.register
def dump(bibname='all', directory='.'):
    if not _os.path.exists(directory):
        runtime_action("'{}' is not a directory".format(directory),
                       action='fail')
    with Bibliography(bibname) as bib:
        path = _os.path.join(directory, '{}.bib'.format(bibname))
        with open(path, 'w') as bibtexfile:
            bibtexfile.write(bib.bibtex())


@commands.register
def create(bibname):
    with Bibliography(bibname, mode='n') as _:
        pass


@commands.register
def delete(bibname):
    with Bibliography(bibname) as bib:
        bib.path.unlink() # pylint: disable=no-member


@commands.register
def activate(bibname):
    with Bibliography(bibname) as bib:
        print(bib)


@commands.register
def show():
    # TODO: get active bibname
    bibname = 'all'
    with Bibliography(bibname) as bib:
        print(bib)


@commands.register
def find(pattern):
    # TODO: get active bibname
    bibname = 'all'
    with Bibliography(bibname) as bib:
        print('\n'.join(map(str, bib.search(pattern))))


@commands.register
def search(pattern):
    # TODO: get active bibname
    bibname = 'all'
    with Bibliography(bibname) as bib:
        print('\n'.join(map(str, bib.search(pattern))))


@commands.register
def gc():
    # TODO: get active bibname
    bibname = 'all'
    with Bibliography(bibname) as bib:
        bib.cleanup()
