#!/bin/env python3.5
# -*- coding: utf-8 -*-
"""
This is the main file of the texbib program. A program that helps you
to manage your BibTeX references.
"""

import argparse

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

    cmd = args.command
    cmd_args = args.args
    cmd_parser = CmdParser(fail, tell)

    if hasattr(cmd_parser, cmd) and not cmd.startswith('__'):
        cmd_func = getattr(cmd_parser, cmd)
        try:
            cmd_func(*cmd_args)
        except TypeError:
            fail('wrong number of arguments')
        except exceptions.BibNameError:
            fail('unknown bibname')
        except exceptions.DatabaseError:
            fail('database currupt')
    else:
        fail('unknown command')

if __name__ == '__main__':
    argp = argparse.ArgumentParser(
        description='Texbib is a program that helps '
        'you to manage your BibTeX references.')

    argp.add_argument('command', help='Texbib command to be executed')
    #choices=('add','addto','show','searchin','rm','rmfrom','mkbib',
    #'rmbib'))

    argp.add_argument(
        'args', nargs='*',
        help='arguments for Texbib command, '
        'number and meaning depends on command')

    main(argp.parse_args())

