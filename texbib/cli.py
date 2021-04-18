#!/bin/env python3.5
# -*- coding: utf-8 -*-
"""
This is the main file of the texbib program. A program that helps you
to manage your BibTeX references.
"""
import argparse
import inspect
import typing

from texbib.runtime import RuntimeInstance
from texbib.commands import commands
from texbib import __version__


def main(args):

    runtime = RuntimeInstance('debug')
    commands.set_runtime(runtime)

    cmds = commands()

    cmd = args['subcommand']
    del args['subcommand']

    cmd_func = cmds[cmd]
    status = cmd_func(**args)

    if status == NotImplemented:
        print('texbib: not implemented')


def parse_args():
    argp = argparse.ArgumentParser(
        prog='texbib',
        description='Texbib is a program that helps '
        'you to manage your BibTeX references.')

    argp.add_argument('--version',
                      action='version',
                      version='%(prog)s ' + __version__)

    subcmdparsers = argp.add_subparsers(dest='subcommand',
                                        help='Texbib command to be executed')

    for cmd in commands.dict:
        subp = subcmdparsers.add_parser(cmd)
        subcmd_sig = inspect.signature(commands.dict[cmd])
        for name, param in subcmd_sig.parameters.items():
            if param.annotation == typing.List[str]:
                subp.add_argument(name, nargs='+')
            elif param.annotation == typing.Union[str, None]:
                subp.add_argument(name, nargs='?')
            else:
                subp.add_argument(name)
    args = argp.parse_args()

    return args.__dict__


def cli():
    main(parse_args())


if __name__ == '__main__':
    cli()
