import re
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional

from .bibliography import Bibliography
from .utils import Levels, Events, rm_tree
from .sources import from_isbn

from .schemes import SCHEMES, EXTENSIONS


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
        parts = obj.split(':')
        if len(parts) > 1 and parts[0] in SCHEMES:
            bibtex, _ = SCHEMES[parts[0]](obj)
        elif re.match('^[0-9-]*$', obj):
            bibtex, _ = from_isbn(obj)
        else:
            path = Path(obj)
            if not path.exists():
                commands.run.event(Events.FileNotFound, path, Levels.error,
                                   Exception('None'))
                continue
            elif path.suffix not in EXTENSIONS:
                raise NotImplementedError
            else:
                bibtex, _ = EXTENSIONS[path.suffix](path)

        if bibtex:
            with commands.run.open('w') as bib:
                added_keys = bib.update(bibtex)
            print('\n'.join(added_keys))
        else:
            print(f'{obj}: no data', file=sys.stderr)


@commands.register
def link_file(identifier: str, filename: str) -> None:
    """Add some resources to the active bibliography"""
    with commands.run.open('w') as bib:
        if identifier in bib:
            path = Path(filename)
            if path.exists():
                shutil.copy(
                    path,
                    bib[identifier].pdf_path(commands.run.active_files_path),
                )
            else:
                commands.run.event(Events.FileNotFound,
                    path, Levels.critical, Exception('None'))
        else:
            commands.run.event(Events.IdNotFound,
                identifier, Levels.critical, Exception('None'))


@commands.register
def rm(objects: List[str]) -> None:
    """Remove a reference from the active bibliography"""
    for identifier in objects:
        try:
            with commands.run.open('w') as bib:
                bib.remove(identifier)
        except KeyError as exc:
            commands.run.event(Events.IdNotFound,
                identifier, Levels.error, exc)


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
            rm_tree(path.parent)
    else:
        commands.run.event(Events.FileNotFound,
                           path,
                           Levels.critical,
                           Exception('None'))


@commands.register
def rename(old_bibname: str, new_bibname: str) -> None:
    """Rename a bibliography"""
    old_path = commands.run.bib_path(old_bibname).parent
    if old_path.exists():
        new_path = commands.run.bib_path(new_bibname).parent
        if not new_path.exists():
            old_path.rename(new_path)
        else:
            commands.run.event(Events.InvalidName,
                               new_path,
                               Levels.critical,
                               Exception('None'))
        if old_bibname == commands.run.active_name:
            commands.run.activate(new_bibname)
    else:
        commands.run.event(Events.FileNotFound,
                           old_path,
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
        if bibpath.is_dir():
            pre = '*' if bibpath.name == commands.run.active_name else ' '
            sys.stdout.write('{} {}\n'.format(pre, bibpath.stem))


@commands.register
def show(bibname: Optional[str] = None) -> None:
    """List the content of the active bibliography"""
    find(patterns=[''], bibname=bibname)


@commands.register
def find(patterns: List[str], bibname: Optional[str] = None) -> None:
    """Seach in local bibliographies"""
    if bibname and not commands.run.is_bib(bibname):
        commands.run.fail(f'Bib "{bibname}" doesn\'t exist.')

    path = commands.run.bib_path(bibname) if bibname \
           else commands.run.active_path
    files_path = commands.run.files_path(bibname) if bibname \
                 else commands.run.active_files_path
    with Bibliography(path, 'r') as bib:
        for bibitem in bib.search(patterns):
            print(bibitem.format_term(has_file=bibitem.pdf_path(files_path).exists()))


@commands.register
def open(obj: str) -> None:
    pdf_path = commands.run.active_files_path/(obj+'.pdf')
    if pdf_path.exists():
        pdf_reader = 'llpp'
        subprocess.run([pdf_reader, pdf_path], check=True)
    else:
        commands.run.event(Events.FileNotFound,
            pdf_path, Levels.critical, Exception('None'))
