import sys
import typing
from pathlib import Path

from texbib.bibliography import Bibliography
from texbib.utils import Levels, Events


class commands(dict): # pylint: disable=invalid-name
    """Utility class to manage cli commands.
    Each command has to be registerd with the classmethod `register`.
    An instance of this class is a dict containing a snapshot
    of the commands registerd at the moment of instanciation.

    The PEP8 violation is intentional.
    Class and instance are to be used the same way.
    """
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
def add(filenames: typing.List[str]) -> None:
    for path in map(Path, filenames):
        if path.exists():
            with path.open() as infile:
                commands.run.active.update(infile.read())
        else:
            commands.run.event(Events.FileNotFound,
                               path,
                               Levels.error,
                               Exception('None'))


@commands.register
def rm(identifyers: typing.List[str]) -> None:
    for identifyer in identifyers:
        try:
            commands.run.active.remove(identifyer)
        except KeyError as exc:
            commands.run.event(Events.IdNotFound,
                               identifyer,
                               Levels.error,
                               exc)


@commands.register
def dump(outfile: typing.Optional[str]=None) -> None:
    if outfile:
        path = Path(outfile)
    else:
        path = Path('./{}.bib'.format(commands.run.active_name))
    with path.open('w') as dumpfile:
        dumpfile.write(commands.run.active.bibtex())


@commands.register
def create(bibname: str) -> None:
    if (not bibname) or (' ' in bibname):
        commands.run.event(Events.InvalidName,
                           repr(bibname),
                           Levels.critical,
                           None)
    else:
        path = commands.run.texbibdir.joinpath('{}.db'.format(bibname))
        if path.exists() and commands.run.ask( # pylint: disable=no-member
                'Bib exists. Overwrite?',
                default=False):
            _ = Bibliography(path, 'n')
        else:
            _ = Bibliography(path, 'c')


@commands.register
def delete(bibname: str) -> None:
    path = commands.run.texbibdir.joinpath('{}.db'.format(bibname))
    if path.exists(): # pylint: disable=no-member
        if commands.run.ask('Realy delete {}?'.format(bibname),
                            default=False):
            path.unlink() # pylint: disable=no-member
    else:
        commands.run.event(Events.FileNotFound,
                           path,
                           Levels.critical,
                           Exception('None'))


@commands.register
def open(bibname: str) -> None:
    path = commands.run.texbibdir.joinpath('{}.db'.format(bibname))
    if str(commands.run.active_path) == str(path):
        commands.run.event(Events.NoEffect, 'already active', Levels.info, None)
    elif path.exists() or commands.run.ask( # pylint: disable=no-member
            'Bib doesn\'t exist. Create it?',
            default=True):
        commands.run.activate(bibname)


@commands.register
def list() -> None:
    for bibpath in commands.run.texbibdir.iterdir():
        if bibpath.suffix == '.db':
            pre = '*' if bibpath.stem in commands.run.active_name else ' '
            sys.stdout.write('{} {}\n'.format(pre, bibpath.stem))


@commands.register
def show(bibname: typing.Optional[str] = None) -> None:
    if bibname:
        return NotImplemented
    else:
        for bibitem in commands.run.active.values():
            sys.stdout.write(str(bibitem) + '\n')


@commands.register
def find(pattern: str) -> None:
    for bibitem in commands.run.active.search(pattern):
        sys.stdout.write(str(bibitem) + '\n')


@commands.register
def search(pattern: str) -> None:
    return NotImplemented


@commands.register
def gc() -> None:
    return NotImplemented
