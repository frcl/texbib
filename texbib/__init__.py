from texbib.bibliography import Bibliography, BibItem
from texbib.commands import commands
from texbib.main import main, parse_args

__all__ = ['Bibliography',
           'BibItem']

__version__ = '0.1.0'

def run_texbib():
    main(parse_args())
