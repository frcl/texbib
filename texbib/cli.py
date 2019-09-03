#!/bin/env python3.5
# -*- coding: utf-8 -*-
"""
This is the main file of the texbib program. A program that helps you
to manage your BibTeX references.
"""
import argparse
import inspect
import typing
from pathlib import Path

from texbib.runtime import RuntimeInstance
from texbib.commands import commands
from texbib import __version__


def main(args):

    runtime = RuntimeInstance(args['debug'])
    del args['debug']
    commands.set_runtime(runtime)

    cmds = commands()

    cmd = args['command']
    del args['command']

    # the validity of the command has already been checked by the ArgumentParser
    try:
        cmd_func = cmds[cmd]
    except KeyError:
        cmd_func = cmds[next(c for c in cmds
                             if c.startswith(cmd) and c != 'delete')]
    status = cmd_func(**args)

    if status == NotImplemented:
        print('bib: not implemented')


def parse_args():
    argp = argparse.ArgumentParser(
        prog='bib',
        description='bib is a program that helps '
        'you to manage your BibTeX references.')

    argp.add_argument('--version', action='version',
                      version='%(prog)s ' + __version__)
    # argp.add_argument('-c', '--config', type=Path)
    argp.add_argument('-d', '--debug', action='store_true')

    subcmdparsers = argp.add_subparsers(title='commands', dest='command',
                                        metavar='command', required=True)

    for cmd in commands.dict:
        cmdhelp = commands.dict[cmd].__doc__
        aliases = [cmd[0]] if cmd != 'delete' else []
        subp = subcmdparsers.add_parser(cmd, help=cmdhelp, aliases=aliases)
        subcmd_sig = inspect.signature(commands.dict[cmd])
        for name, param in subcmd_sig.parameters.items():
            if param.annotation == typing.List[str]:
                subp.add_argument(name, nargs='+')
            elif param.annotation == typing.Union[str, None]:
                subp.add_argument(name, nargs='?')
            elif param.annotation == bool:
                subp.add_argument('-'+name[0], action='store_true')
            else:
                subp.add_argument(name)
    args = argp.parse_args()

    return args.__dict__


def cli():
    main(parse_args())


if __name__ == '__main__':
    cli()
