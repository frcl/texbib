# mypy: disable-error-code="attr-defined"
import os
import re
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
from typing import List, Literal, Optional

from .bibliography import Bibliography, _smart_case
from .errors import FileNotFound, IdNotFound, InvalidName, ExitCode
from .sources import from_isbn
from .parser import loads, dumps
from .schemes import SCHEMES, EXTENSIONS
from .term_utils import tex2term
from .utils import rm_tree


_list = list

_SORT_KEYS = {
    'i': ('ID', '', lambda x: x.lower()),
    'a': ('author', '', lambda x: x.lower()),
    't': ('title', '', tex2term),
    'd': ('year', float('inf'), lambda x: float(x) if x.isdigit() else float('inf')),
}


class commands(dict): # pylint: disable=invalid-name
    """Utility class to manage cli commands.
    Each command has to be registerd with the classmethod `register`.
    An instance of this class is a dict containing a snapshot
    of the commands registerd at the moment of instanciation."""
    cmd_dict: dict[str, object] = {}
    run = None

    def __init__(self):
        super().__init__()
        self.update(self.cmd_dict)

    @classmethod
    def set_runtime(cls, runtime):
        """Set the RuntimeInstance to be used for all commands in this module"""
        cls.run = runtime

    @classmethod
    def register(cls, cmd_func):
        """Register a function for use as subcommand in the cli"""
        cls.cmd_dict[cmd_func.__name__] = cmd_func
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

    Multiple sources can be combined in a single command."""
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

                if path.suffix not in EXTENSIONS:
                    raise NotImplementedError

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
            print(f'{pre} {bibpath.stem}')
    return ExitCode.SUCCESS


@commands.register
def show(bibname: Optional[str] = None,
         sort_by: Optional[Literal['i', 'a', 't', 'd']] = None,
         reverse: bool = False) -> ExitCode:
    """List the content of the active bibliography"""
    find(patterns=[], bibname=bibname, sort_by=sort_by, reverse=reverse)
    return ExitCode.SUCCESS


@commands.register
def detail(identifiers: List[str],
           format: Optional[Literal['simple', 'bibtex']] = None) -> ExitCode:
    """Show detailed information about specific bibliography entries"""
    if format is None:
        format = 'simple'

    status = ExitCode.SUCCESS
    with commands.run.open('r') as bib:
        for identifier in identifiers:
            if identifier in bib:
                print(bib[identifier].format_detail(format_type=format))
            else:
                commands.run.error(str(IdNotFound(identifier)))
                status = ExitCode.ID_NOT_FOUND

    return status


@commands.register
def find(patterns: List[str], bibname: Optional[str] = None,
         sort_by: Optional[Literal['i', 'a', 't', 'd']] = None,
         reverse: bool = False) -> ExitCode:
    """Seach in local bibliographies"""
    if bibname and not commands.run.is_bib(bibname):
        raise FileNotFound(f'Bibliography "{bibname}"')

    path = commands.run.bib_path(bibname) if bibname \
           else commands.run.active_path
    files_path = commands.run.files_path(bibname) if bibname \
                 else commands.run.active_files_path

    ignore_case = _smart_case(patterns)
    with Bibliography(path, 'r') as bib:
        items = _list(bib.search(patterns, ignore_case=ignore_case))
        if sort_by:
            field, default, convert = _SORT_KEYS[sort_by]
            items.sort(key=lambda b: convert(b.get(field, default)), reverse=reverse)
        for bibitem in items:
            print(bibitem.format_term(
                has_file=bibitem.pdf_path(files_path).exists(),
                patterns=patterns,
                ignore_case=ignore_case,
            ))

    return ExitCode.SUCCESS if items else ExitCode.GENERAL_ERROR


@commands.register
def open(obj: str) -> ExitCode:
    """Open local pdf file"""
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
