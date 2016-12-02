#!/bin/env python3.5
# -*- coding: utf-8 -*-
"""
This is the main file of the texbib program. A program that helps you
to manage your BibTeX references.
"""

import argparse
import inspect

from texbib import CmdParser, exceptions

def tell(msg):
    """Print a warning message and continue.
    Used for wranings and if an error is only partial."""
    print('texbib: {}'.format(msg))

def fail(msg):
    """Print error message and exit.
    Used if texbib can not continue."""
    print('texbib: {}'.format(msg))
    quit()

def main(args):

    cmd = args['subcommand']
    del args['subcommand']
    cmd_parser = CmdParser(fail, tell)

    if hasattr(cmd_parser, cmd) and not cmd.startswith('_'):
        cmd_func = getattr(cmd_parser, cmd)
        # try:
        cmd_func(**args)
        # except TypeError:
            # fail('wrong number of arguments')
        # except ValueError:
            # fail('unknown bibname')
        # except IOError:
            # fail('database currupt')
    else:
        fail('unknown command')

def parse_args():
    argp = argparse.ArgumentParser(
        prog='texbib',
        description='Texbib is a program that helps '
        'you to manage your BibTeX references.')

    argp.add_argument('--version', action='version', version='%(prog)s alpha')
    argp.add_argument('-z', '--gen-zsh-comp', action='store_true')

    subcmdparsers = argp.add_subparsers(dest='subcommand',
                                        help='Texbib command to be executed')

    for attr in dir(CmdParser):
        if not attr.startswith('_'):
            subp = subcmdparsers.add_parser(attr)
            subargs = inspect.getargs(getattr(CmdParser, attr).__code__)
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
