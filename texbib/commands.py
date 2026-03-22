import os
import re
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import List, Optional

from .bibliography import Bibliography
from .errors import FileNotFound, IdNotFound, InvalidName, ExitCode
from .sources import from_isbn
from .parser import loads, dumps
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
def add(objects: List[str]) -> ExitCode:
    """Add some resources to the active bibliography

    Supports multiple input formats:
    - Local files: bib add paper.bib
    - DOI: bib add doi:10.1002/andp.19053220806
    - arXiv: bib add arXiv:1306.4856
    - ISBN: bib add 9780123456789
    - stdin: cat paper.bib | bib add -

    Multiple sources can be combined in a single command.
    """
    exit_code = ExitCode.SUCCESS
    for obj in objects:
        if obj == '-':
            # Read BibTeX from stdin
            bibtex = sys.stdin.read()
            if not bibtex.strip():
                print('-: no data from stdin', file=sys.stderr)
                exit_code = ExitCode.GENERAL_ERROR
                continue
        else:
            parts = obj.split(':')
            if len(parts) > 1 and parts[0] in SCHEMES:
                bibtex, _ = SCHEMES[parts[0]](obj)
            elif re.match('^[0-9-]*$', obj):
                bibtex, _ = from_isbn(obj)
            else:
                path = Path(obj)
                if not path.exists():
                    exc = FileNotFound(path)
                    commands.run.error(str(exc))
                    exit_code = exc.exit_code
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
            exit_code = ExitCode.GENERAL_ERROR

    return exit_code


@commands.register
def link_file(identifier: str, filename: str) -> ExitCode:
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
                raise FileNotFound(path)
        else:
            raise IdNotFound(identifier)
    return ExitCode.SUCCESS


@commands.register
def rm(objects: List[str]) -> ExitCode:
    """Remove a reference from the active bibliography"""
    status = ExitCode.SUCCESS
    for identifier in objects:
        try:
            with commands.run.open('w') as bib:
                bib.remove(identifier)
        except KeyError:
            commands.run.error(str(IdNotFound(identifier)))
            status = ExitCode.ID_NOT_FOUND
    return status


@commands.register
def dump(outfile: Optional[str] = None) -> ExitCode:
    """Create a bibtex file with all references in active bibliography"""
    with commands.run.open() as bib:
        if not outfile or outfile == '-':
            sys.stdout.write(bib.bibtex())
        else:
            path = Path(outfile)
            with path.open('w') as dumpfile:
                dumpfile.write(bib.bibtex())
            print(f'Wrote to {path}', file=sys.stderr)
    return ExitCode.SUCCESS


@commands.register
def init(bibname: str) -> ExitCode:
    """Create a new bibliography"""
    if (not bibname) or (' ' in bibname):
        raise InvalidName(repr(bibname), 'name must not be empty or contain spaces')
    else:
        if commands.run.is_bib(bibname):
            if commands.run.ask(f'Bib "{bibname}" exists. '
                                'Overwrite it, deleting all content?',
                                default=False):
                commands.run.bib_path(bibname).unlink()
                commands.run.activate(bibname)
            else:
                print('Aborted.', file=sys.stderr)
                return ExitCode.GENERAL_ERROR
        else:
            commands.run.activate(bibname)
    return ExitCode.SUCCESS


@commands.register
def delete(bibname: str) -> ExitCode:
    """Delete a bibliography"""
    path = commands.run.bib_path(bibname)
    if path.exists():
        if commands.run.ask(f'Really delete "{bibname}"?', default=False):
            from .utils import rm_tree
            rm_tree(path.parent)
        else:
            print('Aborted.', file=sys.stderr)
            return ExitCode.GENERAL_ERROR
    else:
        raise FileNotFound(path)
    return ExitCode.SUCCESS


@commands.register
def rename(old_bibname: str, new_bibname: str) -> ExitCode:
    """Rename a bibliography"""
    old_path = commands.run.bib_path(old_bibname).parent
    if old_path.exists():
        new_path = commands.run.bib_path(new_bibname).parent
        if not new_path.exists():
            old_path.rename(new_path)
        else:
            raise InvalidName(new_bibname, 'target bibliography already exists')
        if old_bibname == commands.run.active_name:
            commands.run.activate(new_bibname)
    else:
        raise FileNotFound(old_path)
    return ExitCode.SUCCESS


@commands.register
def checkout(bibname: str) -> ExitCode:
    """Activate a bibliography"""
    if bibname == commands.run.active_name:
        print(f'Already using "{bibname}"', file=sys.stderr)
    elif commands.run.is_bib(bibname) or commands.run.ask(
            f'Bib "{bibname}" doesn\'t exist. Create it?', default=True):
        commands.run.activate(bibname)
    else:
        print('Aborted.', file=sys.stderr)
        return ExitCode.FILE_NOT_FOUND
    return ExitCode.SUCCESS


@commands.register
def list() -> ExitCode:
    """List all available bibliographies"""
    for bibpath in commands.run.bibdir.iterdir():
        if bibpath.is_dir():
            pre = '*' if bibpath.name == commands.run.active_name else ' '
            print('{} {}'.format(pre, bibpath.stem))
    return ExitCode.SUCCESS


@commands.register
def show(bibname: Optional[str] = None) -> ExitCode:
    """List the content of the active bibliography"""
    find(patterns=[''], bibname=bibname)
    return ExitCode.SUCCESS


@commands.register
def find(patterns: List[str], bibname: Optional[str] = None) -> ExitCode:
    """Seach in local bibliographies"""
    if bibname and not commands.run.is_bib(bibname):
        raise FileNotFound(f'Bibliography "{bibname}"')

    path = commands.run.bib_path(bibname) if bibname \
           else commands.run.active_path
    files_path = commands.run.files_path(bibname) if bibname \
                 else commands.run.active_files_path

    found = False
    with Bibliography(path, 'r') as bib:
        for bibitem in bib.search(patterns):
            print(bibitem.format_term(has_file=bibitem.pdf_path(files_path).exists()))
            found = True

    return ExitCode.SUCCESS if found else ExitCode.GENERAL_ERROR


@commands.register
def open(obj: str) -> ExitCode:
    pdf_path = commands.run.active_files_path/(obj+'.pdf')
    if pdf_path.exists():
        pdf_reader = commands.run.settings['fulltext']['pdf_reader_cmd']
        subprocess.Popen([pdf_reader, pdf_path], start_new_session=True)
    else:
        raise FileNotFound(pdf_path)
    return ExitCode.SUCCESS


@commands.register
def edit(identifier: str) -> ExitCode:
    """Edit a bibliography entry in $EDITOR"""
    editor = commands.run.settings['edit']['editor'] \
        or os.environ.get('EDITOR') \
        or 'nano'

    with commands.run.open('r') as bib, \
        tempfile.NamedTemporaryFile(mode='w', suffix='.bib', delete=False) as tmp:
        tmp_path = Path(tmp.name)
        if identifier not in bib:
            raise IdNotFound(identifier)

        tmp.write(dumps({identifier: bib[identifier]}))

    try:
        subprocess.run([editor, tmp_path], check=True)

        with tmp_path.open() as tmp:
            edited_content = tmp.read()

        edited_entries = loads(edited_content)

        if len(edited_entries) != 1:
            print('Invalid BibTeX change', file=sys.stderr)
            return ExitCode.GENERAL_ERROR

        new_id = next(iter(edited_entries))

        with commands.run.open('w') as bib:
            if identifier in bib:
                bib.remove(identifier)
            bib.update(edited_content)

        print(f'Updated entry: {new_id}', file=sys.stderr)

    finally:
        tmp_path.unlink()

    return ExitCode.SUCCESS
