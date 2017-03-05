import os
import sys
import json
from pathlib import Path
from typing import Optional, Union

from texbib.bibliography import Bibliography
from texbib.utils import Events, Levels


class RuntimeInstance(object):
    """Class for managing the runtime environment for texbib to run in.

    Consturctor Arguments:
    - mode: str
        One of ('prod', 'debug', 'fake')
    - fakedir: pathlib.Path
        If mode is 'fake', used as texbibdir. Ignored otherwise.
    """
    debug_msg = 'texbib: {exc}: {exc_msg} ({level}, {texbib_msg})'
    error_msg = 'texbib: {level} {texbib_msg}'

    input = input

    def __init__(self, mode: str, fakedir: Union[str, Path, None] = None):

        # bool comparrison is faster than string comparrison
        self.debug = bool(mode == 'debug')

        # use fakedir if a fake runtime is requested (for testing)
        if mode == 'fake' and fakedir:
            self.texbibdir = Path(fakedir)
        else:
            self.texbibdir = Path(os.environ.get('TEXBIBDIR', '~/.texbib'))\
                                .expanduser()

        self.state_path = self.texbibdir.joinpath('active')

        # get active bibname
        if self.state_path.exists():
            with self.state_path.open() as state_file:
                self.active_name = json.load(state_file)['bib']
        else:
            self.active_name = 'default'

        # open database
        self.active_path = self.texbibdir.joinpath(self.active_name + '.db')
        self.lock_path = self.texbibdir.joinpath(self.active_name + '.lock')
        self.lock()
        self.active = Bibliography(self.active_path, mode='c')

    def __del__(self):
        self.active.close()
        self.unlock()

    def lock(self):
        """Create a lock in the active bibliography"""
        self.lock_path.touch() # pylint: disable=no-member

    def unlock(self):
        """Destroy the lock in the active bibliography"""
        self.lock_path.unlink() # pylint: disable=no-member

    def activate(self, bibname: str):
        """Use bibliography with name `bibname` as new active bibliography.
        If it does not exist, create it.

        Arguments:
        - bibname: str
        """
        if not bibname:
            raise ValueError('Cannot create bibliography without name')
        self.active.close()
        self.unlock()
        self.active_name = bibname
        self.active_path = self.texbibdir.joinpath(self.active_name + '.db')
        self.lock_path = self.texbibdir.joinpath(self.active_name + '.lock')
        self.lock()
        self.active = Bibliography(self.active_path, 'c')
        with self.state_path.open('w') as state_file: # pylint: disable=no-member
            json.dump({'bib': self.active_name}, state_file)

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
        texbib_msg = f'{event}: {info}'

        if self.debug:
            if exc:
                msg = self.debug_msg.format(exc=type(exc).__name__,
                                            exc_msg=', '.join(exc.args),
                                            level=level,
                                            texbib_msg=texbib_msg)
            else:
                msg = self.debug_msg.format(level=level,
                                            texbib_msg=texbib_msg)
        else:
            msg = self.error_msg.format(level=level,
                                        texbib_msg=event)

        sys.stderr.write(msg)

        if level == Levels.critical:
            sys.stdout.write('aborting...')
            sys.exit(1)

    def ask(self, msg: str, default: bool = True):
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
