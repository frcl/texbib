import re
import sys
from pathlib import Path
from typing import List, Optional

from texbib.bibliography import Bibliography
from texbib.utils import Levels, Events
from texbib.sources import from_doi, from_arxiv, from_isbn


class commands(dict): # pylint: disable=invalid-name
    """Utility class to manage cli commands.
    Each command has to be registerd with the classmethod `register`.
    An instance of this class is a dict containing a snapshot
    of the commands registerd at the moment of instanciation."""
    dict = {}
    run = None

    def __init__(self):
        super(commands, self).__init__()
        self.update(self.dict)

    @classmethod
    def set_runtime(cls, runtime):
        """Set the RuntimeInstance to be used for all commands in this module
        """
        cls.run = runtime

    @classmethod
    def register(cls, cmd_func):
        """Register a function for use as subcommand in the cli
        """
        cls.dict[cmd_func.__name__] = cmd_func
        return cmd_func


@commands.register
def add(objects: List[str]) -> None:
    """Add some resources to the active bibliography"""
    for obj in objects:
        if obj.lower().startswith('doi:') or 'doi.org' in obj:
            try:
                bibtex, pdf_path = from_doi(obj)
            except Exception as exc:
                commands.run.event(Events.FailedAccess, obj,
                                   Levels.error, exc)
                continue
            # if pdf_path:
                # TODO: store pdf_path in database
        elif obj.lower().startswith('arxiv:'):
            print('adding from arxiv not implemented')
            continue
        elif re.match('^[0-9-]*$', obj):
            bibtex, _ = from_isbn(obj)
        else:
            path = Path(obj)
            if path.exists():
                # if path.suffix == '.pdf':
                    # TODO: read metadata from pdf
                # elif path.suffix == '.bib':
                if path.suffix in ('.bib', '.bibtex'):
                    with path.open() as infile:
                        bibtex = infile.read()
            else:
                commands.run.event(Events.FileNotFound, path, Levels.error,
                                   Exception('None'))
                continue
        if bibtex:
            with commands.run.open('w') as bib:
                added_keys = bib.update(bibtex)
            print('\n'.join(added_keys))
            # for bibitem in bibtex:
            #   print(bibitem['id'])


@commands.register
def rm(objects: List[str]) -> None:
    """Remove a reference from the active bibliography"""
    for identifier in objects:
        try:
            with commands.run.open('w') as bib:
                bib.remove(identifier)
        except KeyError as exc:
            commands.run.event(Events.IdNotFound,
                               identifier,
                               Levels.error,
                               exc)


@commands.register
def dump(outfile: Optional[str] = None) -> None:
    """Create a bibtex file with all references in active bibliography"""
    if outfile:
        path = Path(outfile)
    else:
        path = Path(f'./{commands.run.active_name}.bib')
    with path.open('w') as dumpfile, \
         commands.run.open() as bib:
        dumpfile.write(bib.bibtex())
    print(f'Wrote to {path}')


@commands.register
def init(bibname: str) -> None:
    """Create a new bibliography"""
    if (not bibname) or (' ' in bibname):
        commands.run.event(Events.InvalidName,
                           repr(bibname),
                           Levels.critical,
                           None)
    else:
        if commands.run.is_bib(bibname):
            if commands.run.ask(f'Bib "{bibname}" exists. '
                                'Overwrite it, deleting all content?',
                                default=False):
                commands.run.bib_path(bibname).unlink()
                commands.run.activate(bibname)
            else:
                print('Aborted.')
        else:
            commands.run.activate(bibname)


@commands.register
def delete(bibname: str) -> None:
    """Delete a bibliography"""
    path = commands.run.bib_path(bibname)
    if path.exists():
        if commands.run.ask(f'Really delete "{bibname}"?', default=False):
            path.unlink()
    else:
        commands.run.event(Events.FileNotFound,
                           path,
                           Levels.critical,
                           Exception('None'))


@commands.register
def checkout(bibname: str) -> None:
    """Activate a bibliography"""
    if bibname == commands.run.active_name:
        print(f'Already using "{bibname}"')
    elif commands.run.is_bib(bibname) or commands.run.ask(
            f'Bib "{bibname}" doesn\'t exist. Create it?', default=True):
        commands.run.activate(bibname)
    else:
        print('Aborted')


@commands.register
def list() -> None:
    """List all available bibliographies"""
    for bibpath in commands.run.bibdir.iterdir():
        if bibpath.is_dir() and (bibpath/'metadata.db').exists():
            pre = '*' if bibpath.name == commands.run.active_name else ' '
            sys.stdout.write('{} {}\n'.format(pre, bibpath.stem))


@commands.register
def show(bibname: Optional[str] = None) -> None:
    """List the content of the active bibliography"""
    path = commands.run.bib_path(bibname) if bibname \
           else commands.run.active_path
    with Bibliography(path, 'r') as bib:
        for bibitem in bib.values():
            sys.stdout.write(str(bibitem) + '\n')


@commands.register
def find(patterns: List[str]) -> None:
    """Seach in local bibliographies"""
    with commands.run.open() as bib:
        for bibitem in bib.search(patterns):
            sys.stdout.write(str(bibitem) + '\n')
