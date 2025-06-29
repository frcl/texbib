import os
import sys
import json
from pathlib import Path
from typing import Optional
import appdirs

from texbib.bibliography import Bibliography
from texbib.utils import Events, Levels
from texbib.settings import get_settings


class RuntimeInstance:
    """Class for managing the runtime environment for bib to run in.

    Consturctor Arguments:
        debug (bool): Indicate if to run in debug mode
        bibdir (pathlib.Path): base directory for runtime
    """
    debug_msg = 'bib: {exc}: {exc_msg} ({level}, {bib_msg})'
    error_msg = 'bib: {level} {bib_msg}'

    input = input

    def __init__(self, debug: bool, bibdir: Optional[Path] = None, config_path: Optional[Path] = None):

        self.debug = debug

        if bibdir:
            self.bibdir = bibdir
        elif path := os.environ.get('TEXBIBDIR'):
            self.bibdir = Path(path).expanduser()
        else:
            self.bibdir = Path(appdirs.user_config_dir('bib'))

        if not self.bibdir.exists():
            self.bibdir.mkdir(parents=True)

        if config_path and not config_path.exists():
            self.fail('Given config file does not exist')

        self.settings = get_settings(config_path or self.bibdir/'bib.conf')

        # if bd := self.settings['core']['bibdir']:
            # self.bibdir = bd

        self.state_path = self.bibdir/'ACTIVE'

        # read state
        if self.state_path.exists():
            with self.state_path.open() as state_file:
                self.state = json.load(state_file)
        else:
            self.state = {}
            self.activate('default')

    @property
    def active_name(self) -> str:
        return self.state['bib']

    @property
    def active_path(self) -> Path:
        return self.bib_path(self.active_name)

    @property
    def active_files_path(self) -> Path:
        return self.files_path(self.active_name)

    def bib_path(self, bibname) -> Path:
        return self.bibdir/bibname/'data.db'

    def files_path(self, bibname) -> Path:
        return self.bibdir/bibname/'files'

    def is_bib(self, bibname: str) -> bool:
        return self.bib_path(bibname).parent.exists()

    def open(self, mode: str = 'r') -> Bibliography:
        """Open the activate bibliography.
        If it does not exist, create it.

        Arguments:
            mode (str): If 'r' open bib in read mode, if 'w' in write mode

        Returns:
            texbib.Bibliography
        """
        return Bibliography(self.active_path, mode)

    def activate(self, bibname: str):
        """
        Arguments:
            bibname (str): name of the database, must not contain spaces
        """
        if not bibname or ' ' in bibname:
            raise ValueError('Invalid bib name "{}"'.format(bibname))
        self.state['bib'] = bibname
        with self.state_path.open('w') as state_file: # pylint: disable=no-member
            json.dump(self.state, state_file)
        if not self.active_path.exists():
            self.active_path.parent.mkdir(exist_ok=True)
            Bibliography(self.active_path, 'c')
        if not self.active_files_path.exists():
            self.active_files_path.mkdir()

    def event(self, event: Events,
              info: str,
              level: Levels,
              exc: Optional[Exception]):
        """Trigger a runtime event.

        Arguments:
        - event: utils.Events
        - info: str
        - level: utils.Levels
        - exc: Exception
        """
        bib_msg = f'{event}: {info}'

        if self.debug:
            if exc:
                msg = self.debug_msg.format(exc=type(exc).__name__,
                                            exc_msg=', '.join(exc.args),
                                            level=level,
                                            bib_msg=bib_msg)
            else:
                msg = self.error_msg.format(level=level,
                                            bib_msg=bib_msg)
        else:
            msg = self.error_msg.format(level=level,
                                        bib_msg=bib_msg)
        # TODO: message without exception

        sys.stderr.write(msg+'\n')

        if level == Levels.critical:
            sys.stdout.write('aborting...')
            sys.exit(1)

    def ask(self, msg: str, default: bool = True) -> bool:
        """Ask the user a yes/no question and get the answer as bool.

        Arguments:
        - msg: str
        - default: bool
        """
        sys.stdout.write(msg)

        if default:
            sys.stdout.write(' (Y/n) ')
        else:
            sys.stdout.write(' (y/N) ')

        des = self.input()
        return des.lower() == 'y' if des else default

    def fail(self, msg: str):
        print(self.error_msg.format(level='ERROR', bib_msg=msg))
        sys.exit(1)
