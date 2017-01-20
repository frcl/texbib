from .bibliography import Bibliography, BibItem
from .commands import CmdParser
from .main import main, parse_args

__all__ = ['Bibliography',
           'BibItem']
__version__ = '0.1.0a1'

def run_texbib():
    main(parse_args())
