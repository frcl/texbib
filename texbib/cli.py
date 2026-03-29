#!/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main file of the texbib program. A program that helps you
to manage your BibTeX references.
"""
import argparse
import inspect
import sys
import typing
from pathlib import Path
from typing import get_args, get_origin

from texbib.runtime import RuntimeInstance
from texbib.commands import commands
from texbib.errors import BibError, ExitCode
from texbib import __version__


UNALIASED = ['delete', 'rename', 'link_file', 'detail']


def main(args):

    runtime = RuntimeInstance(debug=args['debug'], config_path=args['config'])
    del args['debug']
    del args['config']
    commands.set_runtime(runtime)

    cmds = commands()

    cmd = args['command']
    del args['command']

    # the validity of the command has already been checked by the ArgumentParser
    # TODO: do this with subparser.set_defaults
    try:
        cmd_func = cmds[cmd]
    except KeyError:
        cmd_func = cmds[next(c for c in cmds
                             if c.startswith(cmd) and c not in UNALIASED)]

    try:
        status = cmd_func(**args)
    except BibError as e:
        runtime.error(e.message)
        sys.exit(e.exit_code)
    except NotImplementedError:
        runtime.error('Command not implemented')
        sys.exit(1)
    except Exception as e:
        if runtime.debug:
            import traceback
            traceback.print_exc()
        else:
            runtime.error(f'Unexpected error: {e}')
        sys.exit(1)

    if status == NotImplemented:
        print('bib: not implemented', file=sys.stderr)
        sys.exit(ExitCode.GENERAL_ERROR)

    sys.exit(status or ExitCode.SUCCESS)


def parse_args():
    argp = argparse.ArgumentParser(
        prog='bib',
        description='bib is a program that helps '
        'you to manage your BibTeX references.')

    argp.add_argument('--version', action='version',
                      version='%(prog)s ' + __version__)
    argp.add_argument('-c', '--config', type=Path)
    argp.add_argument('-d', '--debug', action='store_true')

    subcmdparsers = argp.add_subparsers(title='commands', dest='command',
                                        metavar='command', required=True)

    for cmd_name, cmd in commands().items():
        aliases = [cmd_name[0]] if cmd_name not in UNALIASED else []
        subp = subcmdparsers.add_parser(cmd_name, help=cmd.__doc__, aliases=aliases)
        subcmd_sig = inspect.signature(cmd)
        for name, param in subcmd_sig.parameters.items():
            if param.annotation == typing.List[str]:
                # Make list arguments optional to support stdin-only usage
                subp.add_argument(name, nargs='*', metavar=name.upper())
            elif param.annotation == typing.Union[str, None]:
                subp.add_argument(name, nargs='?')
            elif param.annotation == bool:
                short = '-' + name[0]
                long = '--' + name.replace('_', '-')
                subp.add_argument(short, long, action='store_true')
            elif get_origin(param.annotation) is typing.Union and \
                    get_origin(get_args(param.annotation)[0]) is typing.Literal:
                choices = tuple(a for a in get_args(get_args(param.annotation)[0]) if a is not None)
                short = '-' + name[0]
                long = '--' + name.replace('_', '-')
                subp.add_argument(short, long, choices=choices, nargs='?', default=None)
            else:
                subp.add_argument(name)
    args = argp.parse_args()

    return args.__dict__


def cli():
    main(parse_args())


if __name__ == '__main__':
    cli()
