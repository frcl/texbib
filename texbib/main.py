#!/bin/env python3.5
# -*- coding: utf-8 -*-
"""
This is the main file of the texbib program. A program that helps you
to manage your BibTeX references.
"""

import argparse
import inspect

from texbib.commands import commands
from texbib.utils import runtime_action


def main(args):

    cmd = args['subcommand']
    del args['subcommand']

    if cmd in commands:
        cmd_func = commands[cmd]
        # try:
        cmd_func(**args)
        # except TypeError:
            # fail('wrong number of arguments')
        # except ValueError:
            # fail('unknown bibname')
        # except IOError:
            # fail('database currupt')
    else:
        runtime_action('unknown command', action='fail')

def parse_args():
    argp = argparse.ArgumentParser(
        prog='texbib',
        description='Texbib is a program that helps '
        'you to manage your BibTeX references.')

    # argp.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    argp.add_argument('-z', '--gen-zsh-comp', action='store_true')

    subcmdparsers = argp.add_subparsers(dest='subcommand',
                                        help='Texbib command to be executed')

    for attr in commands:
        if not attr.startswith('_'):
            subp = subcmdparsers.add_parser(attr)
            subargs = inspect.getargs(commands[attr].__code__)
            for arg in subargs.args:
                if not arg == 'self':
                    if arg in ('filenames', 'identifyer'):
                        subp.add_argument(arg, nargs='+')
                    else:
                        subp.add_argument(arg)

    args = argp.parse_args()
    if args.gen_zsh_comp:
        try:
            import genzshcomp
            gen = genzshcomp.CompletionGenerator('texbib', argp)
            print(gen.get())
            # TODO: generate bigger compoeltion file from subparsers
        except ImportError:
            print("""The genzshcomp module is requiered
                  install it with `pip install genzshcomp`
                  """)
        exit(0)
    else:
        args = args.__dict__
        del args['gen_zsh_comp']

    return args

if __name__ == '__main__':
    main(parse_args())
